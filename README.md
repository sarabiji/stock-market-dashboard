
# Stock Market Dashboard (FastAPI + Chart.js)

A clean, responsive web app to explore stock price history with a FastAPI backend (serving a simple REST API) and a vanilla HTML/CSS/JS frontend powered by Chart.js. It supports both US and NSE tickers (e.g., `AAPL`, `RELIANCE.NS`).

## Features
- Left panel: scrollable list of 10+ companies
- Main panel: interactive Chart.js line chart
- FastAPI backend with endpoints:
  - `GET /api/companies`
  - `GET /api/history?ticker=...&period=1y&interval=1d&predict=true`
- Live data via `yfinance`
- Stats: last close, 52-week high/low, 30-day average volume, RSI(14)
- Simple AI: linear regression next-day close prediction
- Dockerfile included
- Frontend is served as static files by FastAPI

## Quick Start (Local)
```bash
# 1) Create venv
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install deps
pip install -r backend/requirements.txt

# 3) Run
python backend/main.py
# Visit http://localhost:8000
```

## Docker
```bash
docker build -t stock-dashboard .
docker run -p 8000:8000 stock-dashboard
```

## Deploy (Render/Railway/Vercel)
- Use this repo directly. Set start command: `python backend/main.py`, expose port `8000`.
- On Vercel, you can deploy the frontend separately and host the API on Render/Railway.

## Notes on Data
- The app uses `yfinance`. Some tickers need exchange suffixes (e.g., `.NS` for NSE India).
- A mock dataset `sample_prices.csv` is included for reference/testing.

## Short Note (≈230 words)
**Approach:** I built a minimal, end-to-end dashboard that demonstrates clean separation of concerns: FastAPI provides a thin REST layer for company metadata and historical pricing, while the frontend focuses on UX—quick filtering, responsive layout, and a single, fast line chart. To keep the experience smooth, the API computes useful stats (52W high/low, 30‑day average volume, RSI) server-side and returns them alongside timeseries data. A lightweight linear‑regression baseline supplies a next‑day price prediction to showcase an AI touch without heavy infra.

**Tech:** Backend—FastAPI, yfinance, pandas, scikit‑learn, served with Uvicorn. Frontend—vanilla HTML/CSS/JS with Chart.js. Packaging—Dockerfile for easy containerization. Optional deployment targets include Render/Railway (single container) or Vercel (frontend) + Render (API).

**Challenges:** Stock APIs vary in symbol formats and rate limits; `yfinance` is pragmatic but occasionally returns gaps, so I added input validation and simple fallbacks. Computing technical indicators reliably requires handling NaNs and window sizes; I kept calculations transparent and conservative. Designing a compact yet readable UI on both desktop and mobile pushed me to streamline the layout and avoid over-styling. For prediction, balancing “interesting” with “trustworthy” led me to include a clear, simple baseline rather than overfitting a complex model.
