# IPOVision

<div align="center">

# IPOVision

### Intelligent IPO Analytics Platform with ML-Based Prediction & Real-Time Sentiment Intelligence

<br>

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![React](https://img.shields.io/badge/React-18.2-blue)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange)
![WebSockets](https://img.shields.io/badge/WebSockets-Enabled-yellow)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

</div>

---

# Overview

IPOVision is a modular full-stack IPO analytics platform designed to combine machine learning, sector-aware intelligence, and real-time market sentiment monitoring into a unified financial analytics system.

The platform provides multiple independent analysis engines for evaluating IPO performance potential, market conviction, and sector-specific behavior through an interactive React dashboard backed by FastAPI microservices.

WebApp Link - https://ipo-project-website.vercel.app/

Built by **FEC @ Indian Institute of Technology (IIT) Guwahati**.

---

# Key Features

- **IPO Evaluation Engine:** Predicts IPO return potential using financial and subscription metrics.
- **Deep ML Analysis:** Classification-based inference system with confidence probabilities.
- **Sector-Specific Prediction:** Dynamically routes requests to specialized sector-trained ML models.
- **Real-Time Sentiment Streaming:** Live WebSocket-powered sentiment analytics dashboard.
- **Interactive Visualizations:** Gauge meters, contribution graphs, conviction clusters, and velocity tracking.
- **Modular Backend Architecture:** Independent FastAPI services mounted into a unified backend.
- **Scalable ML Infrastructure:** Supports multiple serialized sklearn pipelines and future model expansion.

---

# System Architecture

IPOVision follows a modular microservices-inspired architecture to ensure clean separation of concerns and scalable deployment.

## 1. Frontend Layer (React + Vite)
- Interactive multi-tab dashboard UI.
- Handles API communication and real-time WebSocket rendering.
- Provides visual analytics for all prediction engines.

## 2. Unified FastAPI Backend
Acts as the central orchestration layer.

### Mounted Services

#### IPO Evaluator Service
- Structured IPO scoring pipeline.
- Financial and subscription analysis.
- Return projection visualization.

#### Deep Analysis Service
- Feature preprocessing and log transformation.
- ML classification pipeline.
- Confidence probability estimation.

#### Sector-Wise Prediction Service
- Sector-aware model routing.
- Specialized ML models for each market sector.
- Dynamic inference system.

#### Sentiment Analysis Service
- Background worker execution.
- WebSocket streaming.
- PostgreSQL LISTEN/NOTIFY integration.
- Live dashboard synchronization.

---

# High-Level Data Flow

```text
Frontend Dashboard (React/Vite)
            │
            ▼
Unified FastAPI Backend
            │
 ┌──────────┼───────────────┬───────────────┬───────────────┐
 ▼          ▼               ▼               ▼
IPO      Deep ML       Sector Models    Sentiment Engine
Engine   Analysis      Routing          (Realtime WS)
```

---

# Sentiment Engine Architecture

The sentiment module uses asynchronous streaming architecture for real-time market intelligence.

```text
User Request
     │
     ▼
FastAPI Endpoint (/sentiment/start)
     │
     ▼
Background Worker Thread
     │
     ▼
PostgreSQL LISTEN / NOTIFY
     │
     ▼
WebSocket Streaming Layer
     │
     ▼
Realtime React Dashboard
```

---

# Tech Stack

## Frontend
- React.js
- Vite
- Tailwind CSS
- Recharts
- WebSockets

## Backend
- FastAPI
- Uvicorn
- AsyncIO
- PostgreSQL
- WebSockets
- Scikit-learn
- Joblib
- Pandas
- NumPy

## Machine Learning
- Random Forest Regressor
- Linear Regression
- Feature Engineering Pipelines
- Sector-Specific Model Training

## Deployment
- Vercel (Frontend)
- Railway / Render / Hugging Face Spaces (Backend)
- GitHub Actions Ready

---

# Project Structure

```text
IPO_PROJECT_WEBSITE/
│
├── backend/
│   │
│   ├── app/                     # IPO Evaluator Service
│   │   ├── services/
│   │   ├── main.py
│   │   ├── schemas.py
│   │   ├── model.pkl
│   │   └── constants.py
│   │
│   ├── deep/                    # Deep Analysis Service
│   │   ├── services/
│   │   ├── main.py
│   │   └── model.pkl
│   │
│   ├── sector/                  # Sector-Wise Prediction Service
│   │   ├── saved_models/
│   │   └── main.py
│   │
│   ├── sentiment/               # Real-Time Sentiment Engine
│   │   ├── worker.py
│   │   ├── main.py
│   │   └── app/
│   │
│   ├── main.py                  # Unified Backend Router
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

# API Endpoints

## IPO Evaluation

```http
POST /ipo/predict
```

---

## Deep Analysis

```http
POST /deep/deep_analysis
```

---

## Sector-Wise Prediction

```http
POST /sector/predict
```

---

## Sentiment Analysis

### Start Worker

```http
POST /sentiment/start
```

### Stop Worker

```http
POST /sentiment/stop
```

### WebSocket Stream

```text
/ws/v_t_stream
```

---

# Installation Guide

## Clone Repository

```bash
git clone https://github.com/Krishieboyy/ipo_project_website.git
cd ipo_project_website
```

---

# Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

---

# Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs on:

```text
http://localhost:8000
```

---

# Environment Variables

## Frontend (.env)

```env
VITE_API_BASE=http://localhost:8000
VITE_WS_BASE=ws://localhost:8000
```

---

# Deployment

## Frontend Deployment (Vercel)

```bash
npm run build
```

Deploy the `frontend` directory to Vercel.

---

## Backend Deployment

### Railway / Render

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

# Future Improvements

- LLM-powered IPO summarization
- RAG-based financial document analysis
- Live NSE/BSE market data ingestion
- Explainable AI dashboards
- User authentication & portfolio tracking
- Historical IPO benchmarking
- Automated financial report parsing

---

# Screenshots

## IPO Evaluator
- Gauge-based return prediction
- Parameter contribution visualization
- Long-term and short-term analysis

## Sentiment Dashboard
- Conviction clustering
- Sentiment velocity tracking
- AI confidence estimation
- Real-time streaming updates

## Sector-Wise Prediction
- Dynamic sector selection
- Sector-specialized inference engine  
