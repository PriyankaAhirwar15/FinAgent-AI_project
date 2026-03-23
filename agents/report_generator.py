from langchain_groq import ChatGroq
from core.state import AgentState
from config import GROQ_API_KEY, MODEL_NAME
from datetime import datetime
import os
llm = ChatGroq(api_key=GROQ_API_KEY, model=MODEL_NAME)
def report_generator_node(state: AgentState) -> AgentState:
    stocks = state.get("stocks", [])
    market_data = state.get("market_data", {})
    sentiment = state.get("news_sentiment", {}).get("sentiment_scores", {})
    portfolio = state.get("portfolio_allocation", {})
    risk = state.get("risk_assessment", {})
    stock_details = []
    for ticker in stocks:
        data = market_data.get(ticker, {})
        sent = sentiment.get(ticker, {})
        risk_info = risk.get("risk_scores", {}).get(ticker, {})
        alloc = portfolio.get("allocations", {}).get(ticker, 0)
        stock_details.append(f"""
### {ticker} - {data.get('company_name', ticker)}
- Current Price: 
- Daily Change: {data.get('change_percent', 'N/A')}%
- Sector: {data.get('sector', 'N/A')}
- News Sentiment: {sent.get('sentiment', 'N/A')}
- Risk Level: {risk_info.get('level', 'N/A')} (Score: {risk_info.get('score', 'N/A')}/10)
- Recommended Allocation: {alloc}%
""")
    report = f"""# FinAgent AI - Investment Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
## Executive Summary
Analyzed {len(stocks)} stocks: {', '.join(stocks)}
Overall Risk: {risk.get('overall_risk', 'N/A').upper()}
Strategy: {portfolio.get('strategy', 'N/A')}
## Stock Analysis
{''.join(stock_details)}
## Portfolio Allocation
{chr(10).join([f'- {k}: {v}%' for k, v in portfolio.get('allocations', {}).items()])}
## Risk Assessment
{risk.get('recommendation', 'N/A')}
## Market Analysis
{market_data.get('analysis', 'N/A')}
---
*This report is for educational purposes only. Not financial advice.*
"""
    os.makedirs("reports/generated", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"reports/generated/report_{timestamp}.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    return {
        "final_report": report,
        "messages": [f"ReportGenerator: Report generated successfully!"],
        "current_agent": "report_generator",
        "next_step": "end"
    }
