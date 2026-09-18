import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def get_stock_data(ticker: str) -> dict:
    try:
        stock = yf.Ticker(ticker)
        info = getattr(stock, "info", {}) or {}
        hist = stock.history(period="1mo")

        if hist is None or hist.empty or "Close" not in hist:
            return {
                "ticker": ticker,
                "company_name": info.get("longName") or info.get("shortName") or ticker,
                "current_price": 0.0,
                "change_percent": 0.0,
                "month_high": 0.0,
                "month_low": 0.0,
                "average_volume": 0,
                "market_cap": info.get("marketCap", "N/A"),
                "pe_ratio": info.get("trailingPE", "N/A"),
                "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
                "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
                "history": {}
            }

        close_series = hist["Close"].dropna()
        if close_series.empty:
            current_price = 0.0
            change_pct = 0.0
            week_high = 0.0
            week_low = 0.0
        else:
            current_price = float(close_series.iloc[-1])
            if len(close_series) >= 2:
                prev_price = float(close_series.iloc[-2])
                change_pct = ((current_price - prev_price) / prev_price * 100) if prev_price != 0 else 0.0
            else:
                change_pct = 0.0
            week_high = float(close_series.max())
            week_low = float(close_series.min())

        avg_vol = 0
        if "Volume" in hist and not hist["Volume"].empty:
            vol_mean = hist["Volume"].mean()
            if not pd.isna(vol_mean):
                avg_vol = int(vol_mean)

        return {
            "ticker": ticker,
            "company_name": info.get("longName") or info.get("shortName") or ticker,
            "current_price": round(current_price, 2),
            "change_percent": round(change_pct, 2),
            "month_high": round(week_high, 2),
            "month_low": round(week_low, 2),
            "average_volume": avg_vol,
            "market_cap": info.get("marketCap", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "history": close_series.tail(30).to_dict()
        }
    except Exception as e:
        return {
            "ticker": ticker,
            "company_name": ticker,
            "current_price": 0.0,
            "change_percent": 0.0,
            "month_high": 0.0,
            "month_low": 0.0,
            "average_volume": 0,
            "sector": "N/A",
            "industry": "N/A",
            "error": str(e)
        }


def get_multiple_stocks(tickers: list) -> dict:
    results = {}
    for ticker in tickers:
        results[ticker] = get_stock_data(ticker)
    return results


if __name__ == "__main__":
    data = get_stock_data("AAPL")
    print(f"Company: {data.get('company_name')}")
    print(f"Price: {data.get('current_price')}")
    print(f"Change: {data.get('change_percent')}%")
    print("Stock tool working!")
