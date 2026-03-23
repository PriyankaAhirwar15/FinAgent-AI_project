from langchain_groq import ChatGroq
from core.state import AgentState
from tools.stock_tool import get_multiple_stocks
from config import GROQ_API_KEY, MODEL_NAME
llm = ChatGroq(api_key=GROQ_API_KEY, model=MODEL_NAME)
def market_researcher_node(state: AgentState) -> AgentState:
    stocks = state.get("stocks", [])
    market_data = get_multiple_stocks(stocks)
    summary_parts = []
    for ticker, data in market_data.items():
        if "error" not in data:
            summary_parts.append(
                f"{ticker}: Price=, "
                f"Change={data['change_percent']}%, "
                f"Sector={data['sector']}"
            )
    prompt = f"""You are a market research analyst.
Analyze this stock data and provide brief insights:
{chr(10).join(summary_parts)}
Provide 2-3 sentences of market analysis."""
    response = llm.invoke(prompt)
    market_data["analysis"] = response.content
    return {
        "market_data": market_data,
        "messages": [f"MarketResearcher: Fetched data for {stocks}"],
        "current_agent": "market_researcher"
    }
