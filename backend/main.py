from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.main import app as ipo_app
from sentiment.main import app as sentiment_app
from sector.main import app as sector_app
from deep.main import app as deep_app

# Main FastAPI application that mounts all microservices
app = FastAPI(title="Combined IPO Backend", version="1.0.0")

# Add CORS middleware to allow cross-origin requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "https://ipo-project-website.vercel.app/",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Main backend is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

# Mount individual service applications
app.mount("/ipo", ipo_app)
app.mount("/sentiment", sentiment_app)
app.mount("/sector", sector_app)
app.mount("/deep", deep_app)