from core.state import AgentState
from tools.stock_tool import get_multiple_stocks
from config import safe_llm_invoke


def market_researcher_node(state: AgentState) -> AgentState:
    stocks = state.get("stocks", [])
    market_data = get_multiple_stocks(stocks)
    summary_parts = []
    for ticker, data in market_data.items():
        if "error" not in data:
            summary_parts.append(
                f"{ticker}: Price=${data.get('current_price', 'N/A')}, "
                f"Change={data.get('change_percent', 'N/A')}%, "
                f"Sector={data.get('sector', 'N/A')}"
            )
    prompt = f"""You are a market research analyst.
Analyze this stock data and provide brief insights:
{chr(10).join(summary_parts)}
Provide 2-3 sentences of market analysis."""
    try:
        response = safe_llm_invoke(prompt)
        market_data["analysis"] = response.content
    except Exception:
        market_data["analysis"] = f"Market data successfully retrieved for {', '.join(stocks)}."

    return {
        "market_data": market_data,
        "messages": [f"MarketResearcher: Fetched data for {stocks}"],
        "current_agent": "market_researcher"
    }
