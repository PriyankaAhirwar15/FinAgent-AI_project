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

    result = {
        "risk_scores": {s: {"score": 5.0, "level": "medium", "factors": "Standard market risk"} for s in stocks},
        "overall_risk": "medium",
        "recommendation": "Diversified asset allocation recommended"
    }

    try:
        response = safe_llm_invoke(prompt)
        json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
        if json_match:
            parsed = json.loads(json_match.group())
            if isinstance(parsed, dict):
                result["overall_risk"] = str(parsed.get("overall_risk", "medium"))
                result["recommendation"] = str(parsed.get("recommendation", result["recommendation"]))
                if isinstance(parsed.get("risk_scores"), dict):
                    clean_scores = {}
                    for s in stocks:
                        r = parsed["risk_scores"].get(s) or parsed["risk_scores"].get(s.lower()) or parsed["risk_scores"].get(s.upper()) or {}
                        if isinstance(r, dict):
                            raw_sc = r.get("score", 5)
                            try:
                                sc = float(raw_sc)
                            except Exception:
                                sc = 5.0
                            lvl = str(r.get("level", "medium")).lower()
                            fct = str(r.get("factors", "Market risk"))
                            clean_scores[s] = {"score": sc, "level": lvl, "factors": fct}
                        else:
                            clean_scores[s] = {"score": 5.0, "level": "medium", "factors": "Market risk"}
                    result["risk_scores"] = clean_scores
    except Exception:
        pass

    return {
        "risk_assessment": result,
        "messages": [f"RiskAssessor: Assessed risk for {stocks}"],
        "current_agent": "risk_assessor"
    }
