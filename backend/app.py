from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import os

app = FastAPI(title="Stock Dashboard API", version="1.0")

# Allow frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend if available
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "../frontend")
if os.path.isdir(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

# ---- Models ----
class Company(BaseModel):
    name: str
    ticker: str

class HistoryPoint(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int

class HistoryResponse(BaseModel):
    company: Company
    period: str
    interval: str
    data: List[HistoryPoint]
    stats: Dict[str, Any]
    prediction: Optional[Dict[str, Any]] = None

# ---- Data ----
COMPANIES = [
    {"name": "Apple", "ticker": "AAPL"},
    {"name": "Microsoft", "ticker": "MSFT"},
    {"name": "Alphabet (Google)", "ticker": "GOOGL"},
    {"name": "Amazon", "ticker": "AMZN"},
    {"name": "NVIDIA", "ticker": "NVDA"},
    {"name": "Meta", "ticker": "META"},
    {"name": "Tesla", "ticker": "TSLA"},
    {"name": "Tata Motors", "ticker": "TATAMOTORS.NS"},
    {"name": "Reliance Industries", "ticker": "RELIANCE.NS"},
    {"name": "HDFC Bank", "ticker": "HDFCBANK.NS"},
    {"name": "Infosys", "ticker": "INFY.NS"},
    {"name": "ICICI Bank", "ticker": "ICICIBANK.NS"},
]

@app.get("/api/companies", response_model=List[Company])
def get_companies():
    return COMPANIES

def compute_stats(df: pd.DataFrame) -> dict:
    stats = {}
    if df.empty:
        return stats
    stats["last_close"] = float(df["Close"].iloc[-1])
    stats["52w_high"] = float(df["High"].rolling(252, min_periods=1).max().iloc[-1])
    stats["52w_low"] = float(df["Low"].rolling(252, min_periods=1).min().iloc[-1])
    stats["avg_volume_30d"] = float(df["Volume"].tail(30).mean()) if len(df) >= 1 else None
    stats["sma_20"] = float(df["Close"].tail(20).mean()) if len(df) >= 20 else None
    stats["sma_50"] = float(df["Close"].tail(50).mean()) if len(df) >= 50 else None
    delta = df["Close"].diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    roll_up = up.rolling(14).mean()
    roll_down = down.rolling(14).mean()
    rs = roll_up / (roll_down + 1e-9)
    rsi = 100.0 - (100.0 / (1.0 + rs))
    stats["rsi_14"] = float(rsi.iloc[-1]) if not rsi.empty else None
    return stats

def simple_lr_forecast(df: pd.DataFrame, horizon: int = 1) -> Optional[dict]:
    if len(df) < 10:
        return None
    closes = df["Close"].tail(60).values.reshape(-1, 1)
    X = np.arange(len(closes)).reshape(-1, 1)
    model = LinearRegression()
    model.fit(X, closes)
    pred = float(model.predict([[len(closes) + horizon - 1]])[0][0])
    return {"model": "LinearRegression", "horizon_days": horizon, "predicted_close": pred}

@app.get("/api/history", response_model=HistoryResponse)
def get_history(ticker: str, period: str = "1y", interval: str = "1d", predict: bool = True):
    try:
        hist = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=False)
        if hist is None or hist.empty:
            raise HTTPException(status_code=404, detail="No data found for ticker")
        hist = hist.rename(columns=str.title)[["Open", "High", "Low", "Close", "Volume"]].dropna()
        daily = yf.download(ticker, period="1y", interval="1d", progress=False, auto_adjust=False)
        daily = daily.rename(columns=str.title) if daily is not None and not daily.empty else hist
        stats = compute_stats(daily)
        data = [{"date": idx.strftime("%Y-%m-%d"), "open": float(r["Open"]), "high": float(r["High"]),
                 "low": float(r["Low"]), "close": float(r["Close"]), "volume": int(r["Volume"])} 
                for idx, r in hist.iterrows()]
        company = next((c for c in COMPANIES if c["ticker"].lower() == ticker.lower()), {"name": ticker, "ticker": ticker})
        resp = {"company": company, "period": period, "interval": interval, "data": data, "stats": stats}
        if predict:
            pred = simple_lr_forecast(daily)
            if pred:
                resp["prediction"] = pred
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.app:app", host="0.0.0.0", port=port, reload=True)
