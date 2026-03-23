import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
def create_price_chart(stock_data: dict) -> str:
    try:
        ticker = stock_data.get("ticker", "")
        history = stock_data.get("history", {})
        if not history:
            return ""
        dates = list(history.keys())
        prices = list(history.values())
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=prices,
            mode="lines+markers",
            name=ticker,
            line=dict(color="#00D4FF", width=2)
        ))
        fig.update_layout(
            title=f"{ticker} - 30 Day Price History",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            template="plotly_dark",
            height=400
        )
        return fig.to_json()
    except Exception as e:
        return ""
def create_portfolio_chart(allocation: dict) -> str:
    try:
        labels = list(allocation.keys())
        values = list(allocation.values())
        fig = px.pie(
            values=values,
            names=labels,
            title="Recommended Portfolio Allocation",
            template="plotly_dark"
        )
        return fig.to_json()
    except Exception as e:
        return ""
if __name__ == "__main__":
    print("Chart tool working!")
