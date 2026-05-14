import torch, time, psycopg2, feedparser
from datetime import datetime
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from urllib.parse import quote
from collections import deque
import yfinance as yf
import sys
import threading

# Database and model configuration
DB_SETTINGS = {"dbname": "postgres", "user": "postgres", "password": "physics", "host": "127.0.0.1", "port": "5432"}
MODEL_ID = "ProsusAI/finbert"
WINDOW_SIZE = 10

# Market signal adjustments for sentiment analysis
MARKET_SIGNALS = {
    "gmp zero": -1.5, "gmp crash": -1.4, "nil gmp": -1.2,
    "lock-in pressure": -1.1, "lower circuit": -1.5,
    "listing day": 0.5, "oversubscribed": 0.3
}

sentiment_buffers = {}
current_ticker = None
worker_thread = None
stop_event = threading.Event()

print("Initializing AI Models...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, use_fast=False)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_ID)
print("Models ready.\n")

def get_smoothed_velocity(ticker, raw_v):
    # Smooth sentiment velocity using moving average
    if ticker not in sentiment_buffers:
        sentiment_buffers[ticker] = deque(maxlen=WINDOW_SIZE)
    buffer = sentiment_buffers[ticker]
    buffer.append(raw_v)
    return sum(buffer) / len(buffer)

def get_vix():
    # Get current VIX value for market regime adjustment
    try:
        return float(yf.Ticker("^INDIAVIX").history(period="1d")['Close'].iloc[-1])
    except:
        return 14.2

def analyze_sentiment(entries, ticker):
    # Analyze sentiment from news headlines using FinBERT
    if not entries:
        return 0.0, 0.0, 0.0, 0.0
    scores = []
    pos_total, neg_total = 0.0, 0.0
    probs = None
    vix = get_vix()
    regime_mult = 1.3 if vix > 15 else 1.0

    for item in entries[:3]:
        text = item.title.lower()
        inputs = tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)

        pos = float(probs[0][1].item())
        neg = float(probs[0][2].item())
        pos_total += pos
        neg_total += neg

        ai_score = pos - neg
        adj = sum(w for sig, w in MARKET_SIGNALS.items() if sig in text)
        scores.append(ai_score + adj)

    raw_v = (sum(scores) / len(scores)) * regime_mult
    smoothed_v = get_smoothed_velocity(ticker, raw_v)
    confidence = float(probs.max().item()) if probs is not None else 0.0
    count = len(entries[:3])

    return round(float(smoothed_v), 4), round(confidence, 2), round(pos_total/count, 4), round(neg_total/count, 4)

def setup_db(conn):
    # Create database table and triggers for sentiment data
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sentiment_velocity_data (
            id SERIAL PRIMARY KEY,
            ticker TEXT,
            velocity FLOAT,
            headline TEXT,
            confidence FLOAT,
            pos FLOAT,
            neg FLOAT,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
    """)
    cur.execute("""
        CREATE OR REPLACE FUNCTION notify_alpha()
        RETURNS trigger AS $$
        DECLARE
            payload JSON;
        BEGIN
            payload := json_build_object(
                'ticker', NEW.ticker,
                'velocity', NEW.velocity,
                'confidence', NEW.confidence,
                'headline', NEW.headline,
                'pos', NEW.pos,
                'neg', NEW.neg,
                'timestamp', NEW.created_at
            );
            PERFORM pg_notify('alpha_channel', payload::text);
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)
    cur.execute("""
        DROP TRIGGER IF EXISTS alpha_trigger ON sentiment_velocity_data;
        CREATE TRIGGER alpha_trigger
        AFTER INSERT ON sentiment_velocity_data
        FOR EACH ROW EXECUTE FUNCTION notify_alpha();
    """)
    conn.commit()
    cur.close()

def run_worker(ipo_name, stop_evt):
    # Main worker function for sentiment analysis
    ticker = ipo_name.upper().replace(" ", "_") + "_IPO"
    search_query = f"{ipo_name} IPO GMP allotment listing share price"
    print(f"\n>>> Starting worker for: {ipo_name} | Ticker: {ticker}")

    conn = psycopg2.connect(**DB_SETTINGS)
    setup_db(conn)
    cur = conn.cursor()

    while not stop_evt.is_set():
        try:
            url = f"https://news.google.com/rss/search?q={quote(search_query)}&hl=en-IN&gl=IN&ceid=IN:en"
            feed = feedparser.parse(url)

            if not feed.entries:
                print("No news found. Retrying in 15s...")
                stop_evt.wait(15)
                continue

            headline = feed.entries[0].title
            v, conf, pos, neg = analyze_sentiment(feed.entries, ticker)

            cur.execute(
                "INSERT INTO sentiment_velocity_data (ticker, velocity, headline, confidence, pos, neg) VALUES (%s, %s, %s, %s, %s, %s)",
                (ticker, v, headline, conf, pos, neg)
            )
            conn.commit()

            trend = "▲ BULLISH" if v > 0.05 else "▼ BEARISH" if v < -0.05 else "● NEUTRAL"
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {ticker} | Velocity: {v:+.4f} | Conf: {conf:.2f} | {trend}")
            print(f"  Headline: {headline[:90]}...\n")

        except Exception as e:
            print(f"[ERROR] {e}")
            try:
                conn.rollback()
            except:
                pass

        stop_evt.wait(15)

    cur.close()
    conn.close()
    print(f"[!] Worker stopped for {ticker}")