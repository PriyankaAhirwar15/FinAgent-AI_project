from typing import TypedDict, Annotated, List, Dict, Any
import operator
class AgentState(TypedDict):
    # User input
    query: str
    stocks: List[str]
    # Agent outputs
    market_data: Dict[str, Any]
    news_sentiment: Dict[str, Any]
    portfolio_allocation: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    final_report: str
    # Control flow
    messages: Annotated[List[str], operator.add]
    current_agent: str
    error: str
    retry_count: int
    next_step: str
