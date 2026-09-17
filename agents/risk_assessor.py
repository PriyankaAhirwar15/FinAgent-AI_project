import json
import re
from core.state import AgentState
from config import safe_llm_invoke


def risk_assessor_node(state: AgentState) -> AgentState:
    stocks = state.get("stocks", [])
    market_data = state.get("market_data", {})
    sentiment = state.get("news_sentiment", {}).get("sentiment_scores", {})
    stock_summary = []
    for ticker in stocks:
        data = market_data.get(ticker, {})
        sent = sentiment.get(ticker, {})
        stock_summary.append(
            f"{ticker}: Change={data.get('change_percent', 'N/A')}%, "
            f"52W High={data.get('52_week_high', 'N/A')}, "
            f"52W Low={data.get('52_week_low', 'N/A')}, "
            f"Sentiment={sent.get('sentiment', 'neutral')}"
        )
    prompt = f"""You are a financial risk assessment expert.
Analyze risk for these stocks:
{chr(10).join(stock_summary)}
Respond with JSON only:
{{"risk_scores": {{{", ".join([f'"{s}": {{"score": 1-10, "level": "low/medium/high", "factors": "brief reason"}}' for s in stocks])}}}, "overall_risk": "low/medium/high", "recommendation": "brief recommendation"}}"""
    try:
        response = safe_llm_invoke(prompt)
        json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = {
                "risk_scores": {s: {"score": 5, "level": "medium", "factors": "Standard market risk"} for s in stocks},
                "overall_risk": "medium",
                "recommendation": "Diversified investment recommended"
            }
    except Exception:
        result = {
            "risk_scores": {s: {"score": 5, "level": "medium", "factors": "Standard market risk"} for s in stocks},
            "overall_risk": "medium",
            "recommendation": "Diversified investment recommended"
        }
    return {
        "risk_assessment": result,
        "messages": [f"RiskAssessor: Assessed risk for {stocks}"],
        "current_agent": "risk_assessor"
    }
