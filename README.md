# Stock Market Dashboard (FastAPI + Chart.js)

A responsive web app to explore stock price history using **FastAPI** as the backend and vanilla **HTML/CSS/JS** with **Chart.js** on the frontend. Supports US and NSE tickers (e.g., `AAPL`, `RELIANCE.NS`).

---

## Live Demo

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Click%20Here-blue?style=for-the-badge)](https://stock-market-dashboard-1-nj8v.onrender.com)

A live version of this dashboard is deployed and can be accessed via the link above.

---

## Development Approach, Technologies, and Challenges

For my Stock Market Dashboard project, I focused on building a clean, end-to-end solution that separates backend logic from frontend presentation. I designed the backend using FastAPI, which exposes endpoints for company data and historical stock prices. The API also calculates key stats—like last close, 52-week high/low, 30-day average volume, and RSI(14)—and includes a simple linear regression model for next-day price prediction.

On the frontend, I used vanilla HTML, CSS, and JavaScript with Chart.js to create a responsive, interactive interface. Users can search/filter companies and see dynamic charts with stats, making the experience smooth and informative.

The project uses Python, pandas, yfinance, and scikit-learn on the backend, while the frontend is lightweight and fast. I containerized everything with Docker for easy deployment on platforms like Render or Railway.

Key challenges I faced included handling different stock symbol formats between US and NSE markets, managing missing or irregular data from yfinance, and computing technical indicators reliably without errors. On the frontend, designing a compact, readable layout that works well on desktop and mobile required careful planning.

Through this project, I learned how to integrate real-world data APIs with Python, compute financial analytics efficiently, and build a user-friendly visualization from scratch. I also gained experience in full-stack deployment using Docker and cloud platforms, as well as debugging asynchronous data flows and ensuring consistent frontend-backend communication. This project strengthened my skills in data-driven UI design, API development, and end-to-end system integration, which I can carry forward into future full-stack and data-focused projects.

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








