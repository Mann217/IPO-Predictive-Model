from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import asyncpg
import asyncio
import threading

from sentiment import worker

# FastAPI app for real-time sentiment analysis
app = FastAPI(title="Sentiment Analysis API", version="1.0.0")

# Database configuration for PostgreSQL
DB_CONFIG = {
    "user": "postgres",
    "password": "physics",
    "database": "postgres",
    "host": "127.0.0.1",
}


class IPORequest(BaseModel):
    ipo_name: str


@app.get("/")
async def root():
    return {"message": "Sentiment module running"}


@app.post("/start")
async def start_worker(req: IPORequest):
    # Stop existing worker if running
    if worker.worker_thread and worker.worker_thread.is_alive():
        worker.stop_event.set()
        worker.worker_thread.join(timeout=5)

    # Start new worker thread for sentiment analysis
    worker.stop_event = threading.Event()
    worker.worker_thread = threading.Thread(
        target=worker.run_worker,
        args=(req.ipo_name, worker.stop_event),
        daemon=True,
    )
    worker.worker_thread.start()

    return {"status": "started", "ipo": req.ipo_name}


@app.post("/stop")
async def stop_worker():
    # Stop the sentiment analysis worker
    if worker.worker_thread and worker.worker_thread.is_alive():
        worker.stop_event.set()
        return {"status": "stopped"}
    return {"status": "not running"}


@app.websocket("/ws/v_t_stream")
async def websocket_endpoint(websocket: WebSocket):
    # WebSocket endpoint for real-time sentiment streaming
    await websocket.accept()
    print("SUCCESS: Browser connected to WebSocket!")

    conn = await asyncpg.connect(**DB_CONFIG)

    async def send_payload(payload: str):
        try:
            await websocket.send_text(payload)
        except Exception as e:
            print(f"WebSocket send failed: {e}")

    def callback(connection, pid, channel, payload):
        # Callback for PostgreSQL LISTEN/NOTIFY
        print(f"DB Signal Received: {payload}")
        asyncio.create_task(send_payload(payload))

    await conn.add_listener("alpha_channel", callback)

    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("Browser disconnected.")
    finally:
        await conn.remove_listener("alpha_channel", callback)
        await conn.close()