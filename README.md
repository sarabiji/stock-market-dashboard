# Stock Market Dashboard (FastAPI + Chart.js)

A responsive web app to explore stock price history using **FastAPI** as the backend and vanilla **HTML/CSS/JS** with **Chart.js** on the frontend. Supports US and NSE tickers (e.g., `AAPL`, `RELIANCE.NS`).

---

## Live Demo

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Click%20Here-blue?style=for-the-badge)](https://stock-market-dashboard-1-nj8v.onrender.com)

A live version of this dashboard is deployed and can be accessed via the link above.

---

## Features

-   Scrollable company list with search/filter.
-   Interactive Chart.js line chart for stock prices.
-   FastAPI endpoints:
    -   `GET /api/companies` – list of companies
    -   `GET /api/history?ticker=...&period=1y&interval=1d&predict=true` – historical data + stats + next-day price prediction
-   Live stock data via `yfinance`.
-   Key Stats: last close, 52-week high/low, 30-day avg volume, RSI(14).
-   Simple linear regression for next-day close price prediction.
-   `Dockerfile` included for containerization.

---

## Tech Stack

-   **Backend:** FastAPI, yfinance, pandas, scikit-learn, Uvicorn
-   **Frontend:** HTML/CSS/JS, Chart.js
-   **Deployment:** Render, Railway, or Vercel + Render API

---

## Project Structure

```
project-root/
├── backend/ # FastAPI API code
├── frontend/ # HTML, CSS, JS, Chart.js
├── Dockerfile # Containerize backend + frontend
└── README.md
```

---

## Setup

### Clone the repo

```bash
git clone <repo-url>
cd stock-market-dashboard
```

### Install backend dependencies

```bash
pip install -r backend/requirements.txt
```

### Run locally

```bash
uvicorn backend.app:app --reload --port 8000
```

Access the frontend at `http://localhost:8000`.

---

## Docker

### Build the image

```bash
docker build -t stock-dashboard .
```

### Run the container

```bash
docker run -p 8000:8000 stock-dashboard
```

---

## Short Note

This is a minimal end-to-end dashboard demonstrating a clean separation of concerns:

-   **Backend** computes stats (52W high/low, avg volume, RSI) and linear regression prediction.
-   **Frontend** handles the UX: filtering, responsive layout, and the interactive chart.

The application is designed to handle stock symbol variations, API gaps, and NaN values gracefully.
