import json
import re
from core.state import AgentState
from config import safe_llm_invoke


def portfolio_optimizer_node(state: AgentState) -> AgentState:
    stocks = state.get("stocks", [])
    market_data = state.get("market_data", {})
    sentiment = state.get("news_sentiment", {}).get("sentiment_scores", {})
    stock_summary = []

    for ticker in stocks:
        data = market_data.get(ticker, {})
        sent = sentiment.get(ticker, {})
        stock_summary.append(
            f"{ticker}: Price=${data.get('current_price', 'N/A')}, "
            f"Change={data.get('change_percent', 'N/A')}%, "
            f"Sentiment={sent.get('sentiment', 'neutral')}, "
            f"PE={data.get('pe_ratio', 'N/A')}"
        )

    prompt = f"""You are a portfolio optimization expert.
Stocks: {chr(10).join(stock_summary)}
Create an optimal portfolio allocation that totals 100%.
Respond with JSON only:
{{"allocations": {{{", ".join([f'"{s}": percentage' for s in stocks])}}}, "strategy": "brief strategy explanation"}}
Replace percentage with actual numbers that sum to 100."""

    equal_split = round(100.0 / max(len(stocks), 1), 1)
    result = {
        "allocations": {s: equal_split for s in stocks},
        "strategy": "Balanced diversification strategy"
    }

    try:
        response = safe_llm_invoke(prompt)
        json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
        if json_match:
            parsed = json.loads(json_match.group())
            if isinstance(parsed, dict) and "allocations" in parsed:
                result["strategy"] = str(parsed.get("strategy", result["strategy"]))
                clean_allocs = {}
                for s in stocks:
                    raw = parsed["allocations"].get(s) or parsed["allocations"].get(s.lower()) or parsed["allocations"].get(s.upper())
                    try:
                        if isinstance(raw, str):
                            raw = raw.replace("%", "").strip()
                        clean_allocs[s] = float(raw) if raw is not None else equal_split
                    except Exception:
                        clean_allocs[s] = equal_split
                result["allocations"] = clean_allocs
    except Exception:
        pass

    return {
        "portfolio_allocation": result,
        "messages": [f"PortfolioOptimizer: Optimized allocation for {stocks}"],
        "current_agent": "portfolio_optimizer"
    }
