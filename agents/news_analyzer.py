import json
import re
from core.state import AgentState
from tools.news_tool import get_stock_news
from config import safe_llm_invoke


def news_analyzer_node(state: AgentState) -> AgentState:
    stocks = state.get("stocks", [])
    market_data = state.get("market_data", {})
    all_news = {}
    sentiment_scores = {}
    for ticker in stocks:
        company_name = market_data.get(ticker, {}).get("company_name", ticker)
        news_data = get_stock_news(ticker, company_name)
        all_news[ticker] = news_data
        news_text = " ".join([
            n.get("content", "") 
            for n in news_data.get("news", [])
        ])
        if news_text:
            prompt = f"""Analyze sentiment for {ticker} stock based on news:
{news_text[:500]}
Respond with JSON only:
{{"sentiment": "positive/negative/neutral", "score": 0.0-1.0, "summary": "one sentence"}}"""
            try:
                response = safe_llm_invoke(prompt)
                json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
                if json_match:
                    sentiment_scores[ticker] = json.loads(json_match.group())
                else:
                    sentiment_scores[ticker] = {"sentiment": "neutral", "score": 0.5, "summary": "No clear sentiment"}
            except Exception:
                sentiment_scores[ticker] = {"sentiment": "neutral", "score": 0.5, "summary": "Analysis unavailable"}
        else:
            sentiment_scores[ticker] = {"sentiment": "neutral", "score": 0.5, "summary": "No news found"}
    return {
        "news_sentiment": {"news": all_news, "sentiment_scores": sentiment_scores},
        "messages": [f"NewsAnalyzer: Analyzed sentiment for {stocks}"],
        "current_agent": "news_analyzer"
    }
