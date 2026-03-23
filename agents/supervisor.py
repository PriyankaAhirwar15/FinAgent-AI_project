from langchain_groq import ChatGroq
from core.state import AgentState
from config import GROQ_API_KEY, MODEL_NAME
import re
llm = ChatGroq(api_key=GROQ_API_KEY, model=MODEL_NAME)
def supervisor_node(state: AgentState) -> AgentState:
    query = state.get("query", "")
    stocks = state.get("stocks", [])
    prompt = f"""You are a financial analysis supervisor.
User query: {query}
Stocks to analyze: {stocks}
Your job is to confirm the analysis plan.
Respond with: PROCEED_WITH_ANALYSIS
Keep response brief."""
    response = llm.invoke(prompt)
    return {
        "messages": [f"Supervisor: Analysis started for {stocks}"],
        "current_agent": "supervisor",
        "next_step": "market_researcher",
        "retry_count": state.get("retry_count", 0),
        "error": ""
    }
