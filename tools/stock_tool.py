import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
def get_stock_data(ticker: str) -> dict:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="1mo")
        if hist.empty:
            return {"error": f"No data found for {ticker}"}
        current_price = hist["Close"].iloc[-1]
        prev_price = hist["Close"].iloc[-2]
        change_pct = ((current_price - prev_price) / prev_price) * 100
        week_high = hist["Close"].max()
        week_low = hist["Close"].min()
        avg_volume = hist["Volume"].mean()
        return {
            "ticker": ticker,
            "company_name": info.get("longName", ticker),
            "current_price": round(current_price, 2),
            "change_percent": round(change_pct, 2),
            "month_high": round(week_high, 2),
            "month_low": round(week_low, 2),
            "average_volume": int(avg_volume),
            "market_cap": info.get("marketCap", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "history": hist["Close"].tail(30).to_dict()
        }
    except Exception as e:
        return {"error": str(e), "ticker": ticker}
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
