import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import json
API_URL = "http://localhost:8000"
st.set_page_config(
    page_title="FinAgent AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #00D4FF;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #888;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #1E1E2E;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #333;
        margin: 0.5rem 0;
    }
    .positive { color: #00FF88; }
    .negative { color: #FF4444; }
    .neutral  { color: #FFD700; }
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="main-header">💰 FinAgent AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">6-Agent Stock Market Analyzer powered by Groq LLM</div>', unsafe_allow_html=True)
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/stock-market.png", width=80)
    st.title("FinAgent AI")
    st.markdown("---")
    st.markdown("### How It Works")
    st.markdown("""
    1. Enter stock tickers
    2. Click Analyze
    3. Get AI-powered insights!
    **6 Specialized Agents:**
    - Supervisor
    - Market Researcher
    - News Analyzer
    - Portfolio Optimizer
    - Risk Assessor
    - Report Generator
    """)
    st.markdown("---")
    st.markdown("### Example Tickers")
    st.code("AAPL, TSLA, GOOGL, MSFT, AMZN")
st.markdown("### Enter Stocks To Analyze")
col1, col2 = st.columns([3, 1])
with col1:
    stocks_input = st.text_input(
        "Stock Tickers (comma separated)",
        placeholder="e.g. AAPL, TSLA, GOOGL",
        label_visibility="collapsed"
    )
with col2:
    analyze_btn = st.button("Analyze", type="primary", use_container_width=True)
query = st.text_input(
    "Analysis Query (optional)",
    placeholder="e.g. Which stock is best for long term investment?",
    value="Provide comprehensive stock analysis and investment recommendations"
)
if analyze_btn and stocks_input:
    stocks = [s.strip().upper() for s in stocks_input.split(",") if s.strip()]
    if not stocks:
        st.error("Please enter at least one stock ticker!")
    else:
        with st.spinner(f"Analyzing {', '.join(stocks)} with 6 AI agents..."):
            try:
                response = requests.post(
                    f"{API_URL}/analyze",
                    json={"query": query, "stocks": stocks},
                    timeout=120
                )
                if response.status_code == 200:
                    data = response.json()
                    st.success("Analysis Complete!")
                    market_data = data.get("market_data", {})
                    portfolio = data.get("portfolio_allocation", {})
                    risk = data.get("risk_assessment", {})
                    st.markdown("---")
                    st.markdown("## Stock Overview")
                    cols = st.columns(len(stocks))
                    for i, ticker in enumerate(stocks):
                        stock_info = market_data.get(ticker, {})
                        if stock_info and "error" not in stock_info:
                            change = stock_info.get("change_percent", 0)
                            color = "positive" if change >= 0 else "negative"
                            arrow = "▲" if change >= 0 else "▼"
                            with cols[i]:
                                st.markdown(f"""
                                <div class="metric-card">
                                    <h3>{ticker}</h3>
                                    <h2></h2>
                                    <p class="{color}">{arrow} {change}%</p>
                                    <p>Sector: {stock_info.get('sector', 'N/A')}</p>
                                </div>
                                """, unsafe_allow_html=True)
                    st.markdown("---")
                    col_left, col_right = st.columns(2)
                    with col_left:
                        st.markdown("### Portfolio Allocation")
                        allocations = portfolio.get("allocations", {})
                        if allocations:
                            fig = px.pie(
                                values=list(allocations.values()),
                                names=list(allocations.keys()),
                                title="Recommended Portfolio",
                                template="plotly_dark"
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            st.info(f"Strategy: {portfolio.get('strategy', 'N/A')}")
                    with col_right:
                        st.markdown("### Risk Assessment")
                        risk_scores = risk.get("risk_scores", {})
                        if risk_scores:
                            for ticker, risk_info in risk_scores.items():
                                level = risk_info.get("level", "medium")
                                score = risk_info.get("score", 5)
                                color = "green" if level == "low" else "orange" if level == "medium" else "red"
                                st.markdown(f"**{ticker}** — Risk: :{color}[{level.upper()}] ({score}/10)")
                                st.progress(score/10)
                                st.caption(risk_info.get("factors", ""))
                        overall = risk.get("overall_risk", "medium")
                        st.markdown(f"**Overall Risk: {overall.upper()}**")
                        st.markdown(f"*{risk.get('recommendation', '')}*")
                    st.markdown("---")
                    st.markdown("### Full Investment Report")
                    report = data.get("report", "")
                    if report:
                        st.markdown(report)
                        st.download_button(
                            label="Download Report",
                            data=report,
                            file_name=f"finagent_report.md",
                            mime="text/markdown"
                        )
                    st.markdown("---")
                    st.markdown("### Agent Pipeline Log")
                    messages = data.get("messages", [])
                    for msg in messages:
                        st.text(msg)
                else:
                    st.error(f"Error: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to API! Make sure FastAPI is running on port 8000!")
            except Exception as e:
                st.error(f"Error: {str(e)}")
elif analyze_btn and not stocks_input:
    st.warning("Please enter stock tickers first!")
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#888'>FinAgent AI — Built with LangGraph + Groq + FastAPI + Streamlit</div>",
    unsafe_allow_html=True
)
