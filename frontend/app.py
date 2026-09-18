import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import json
import os
import threading

# ─────────────────────────────────────────────
# Helper functions for absolute null-safety
# ─────────────────────────────────────────────
def safe_float(val, default=0.0) -> float:
    if val is None:
        return default
    try:
        if isinstance(val, str):
            val = val.replace("%", "").replace("$", "").replace(",", "").strip()
        f = float(val)
        return default if (f != f) else f  # check NaN
    except Exception:
        return default

def safe_int(val, default=0) -> int:
    try:
        return int(safe_float(val, float(default)))
    except Exception:
        return default

# ─────────────────────────────────────────────
# Backend API URL (configurable via env var or default)
# ─────────────────────────────────────────────
API_URL = os.getenv("API_URL", "https://finagent-api-upgrade.onrender.com").rstrip("/")

# ─────────────────────────────────────────────
# Wake up backend silently when page loads
# ─────────────────────────────────────────────
def wake_backend():
    try:
        requests.get(f"{API_URL}/health", timeout=15)
    except Exception:
        pass

threading.Thread(target=wake_backend, daemon=True).start()

# ─────────────────────────────────────────────
# Page configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="FinAgent AI — Multi-Agent Market Intelligence",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# Enhanced UI/UX Custom Styling
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .hero-container {
        text-align: center;
        padding: 1.5rem 0 2rem 0;
        background: linear-gradient(180deg, rgba(0, 212, 255, 0.05) 0%, rgba(0,0,0,0) 100%);
        border-radius: 16px;
        margin-bottom: 2rem;
    }
    
    .hero-title {
        font-size: 2.75rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00D4FF 0%, #7928CA 50%, #FF0080 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #94A3B8;
        max-width: 650px;
        margin: 0 auto;
        font-weight: 400;
    }
    
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 1.25rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(0, 212, 255, 0.3);
    }
    .metric-ticker {
        font-size: 1.1rem;
        font-weight: 700;
        color: #F8FAFC;
        margin: 0;
    }
    .metric-company {
        font-size: 0.8rem;
        color: #94A3B8;
        margin-bottom: 0.5rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .metric-price {
        font-size: 1.75rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 0.25rem 0;
    }
    .positive { color: #10B981; font-weight: 600; font-size: 0.95rem; }
    .negative { color: #EF4444; font-weight: 600; font-size: 0.95rem; }
    .neutral  { color: #F59E0B; font-weight: 600; font-size: 0.95rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Header Hero Section
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <div class="hero-title">💰 FinAgent AI</div>
    <div class="hero-subtitle">
        Autonomous 6-Agent Stock Market Intelligence & Portfolio Optimization
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/stock-market.png", width=70)
    st.markdown("### 🤖 FinAgent AI")
    st.caption("Powered by LangGraph & Groq LLM")
    
    st.markdown("---")
    st.markdown("#### ⚡ 6-Agent Pipeline")
    agents = [
        ("🎯 Supervisor", "Workflow coordinator"),
        ("📊 Market Researcher", "Live financial data"),
        ("📰 News Analyzer", "Tavily web sentiment"),
        ("💼 Portfolio Optimizer", "Weight allocation"),
        ("⚠️ Risk Assessor", "Multi-factor risk score"),
        ("📄 Report Generator", "Synthesis & reporting")
    ]
    for name, desc in agents:
        st.markdown(f"**{name}**  \n<span style='font-size:0.8rem;color:#94A3B8'>{desc}</span>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 💡 Quick Ticker Presets")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        if st.button("Tech Giants", use_container_width=True):
            st.session_state["preset_input"] = "AAPL, MSFT, GOOGL, NVDA"
    with col_p2:
        if st.button("EV & Energy", use_container_width=True):
            st.session_state["preset_input"] = "TSLA, RIVN, ENPH, NEE"

    st.markdown("---")
    st.markdown("#### 🌐 Backend Gateway")
    st.caption(f"Endpoint: `{API_URL}`")
    
    if st.button("🔄 Check Backend Health", use_container_width=True):
        with st.spinner("Connecting to backend..."):
            try:
                r = requests.get(f"{API_URL}/health", timeout=30)
                if r.status_code == 200:
                    st.success("🟢 Backend is online & responsive!")
                else:
                    st.warning(f"🟡 Backend returned status {r.status_code}")
            except Exception:
                st.error("🔴 Backend is waking up. Please allow ~20-30s on free tiers.")

# ─────────────────────────────────────────────
# Input Controls
# ─────────────────────────────────────────────
default_stocks = st.session_state.get("preset_input", "TSLA, RIVN, ENPH, NEE")

st.markdown("##### 🔍 Select Stocks to Analyze")
col_input, col_action = st.columns([3.5, 1])

with col_input:
    stocks_input = st.text_input(
        "Enter Stock Tickers (comma separated)",
        value=default_stocks,
        placeholder="e.g. AAPL, TSLA, GOOGL, MSFT, NVDA",
        label_visibility="collapsed"
    )

with col_action:
    analyze_btn = st.button("🚀 Analyze Stocks", type="primary", use_container_width=True)

query = st.text_input(
    "🎯 Custom Analysis Query / Goal (Optional)",
    placeholder="e.g. Which stock is best for a 3-year growth portfolio?",
    value="Which stock is best for long term investment"
)

# ─────────────────────────────────────────────
# Execution & Results
# ─────────────────────────────────────────────
if analyze_btn:
    raw_tickers = [s.strip().upper() for s in stocks_input.split(",") if s.strip()]

    if not raw_tickers:
        st.warning("⚠️ Please provide at least one valid stock ticker (e.g., AAPL).")
    else:
        with st.status(f"🤖 Orchestrating 6 AI Agents for {', '.join(raw_tickers)}...", expanded=True) as status_box:
            st.write("🎯 **Supervisor**: Initiating multi-agent graph...")
            try:
                response = requests.post(
                    f"{API_URL}/analyze",
                    json={"query": query, "stocks": raw_tickers},
                    timeout=120
                )

                if response.status_code == 200:
                    data = response.json()
                    status_box.update(label="✅ Analysis completed successfully!", state="complete", expanded=False)
                    
                    market_data = data.get("market_data", {}) or {}
                    portfolio   = data.get("portfolio_allocation", {}) or {}
                    risk        = data.get("risk_assessment", {}) or {}
                    report      = data.get("report", "") or ""
                    messages    = data.get("messages", []) or []

                    # ── 1. Stock Overview Grid ──
                    st.markdown("### 📊 Market Snapshot")
                    cols = st.columns(len(raw_tickers))

                    for i, ticker in enumerate(raw_tickers):
                        info = market_data.get(ticker, {})
                        with cols[i]:
                            if info and isinstance(info, dict) and "error" not in info:
                                change = safe_float(info.get("change_percent"), 0.0)
                                is_pos = change >= 0.0
                                color_cls = "positive" if is_pos else "negative"
                                arrow = "▲" if is_pos else "▼"
                                raw_price = info.get("current_price")
                                price_display = f"{safe_float(raw_price):.2f}" if raw_price not in [None, "N/A", ""] else "N/A"
                                company = info.get("company_name") or ticker
                                sector = info.get("sector") or "N/A"

                                st.markdown(f"""
                                <div class="metric-card">
                                    <p class="metric-ticker">{ticker}</p>
                                    <p class="metric-company" title="{company}">{company}</p>
                                    <div class="metric-price">${price_display}</div>
                                    <span class="{color_cls}">{arrow} {change:.2f}% (1M)</span>
                                    <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 0.5rem;">
                                        Sector: <b>{sector}</b>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown(f"""
                                <div class="metric-card">
                                    <p class="metric-ticker">{ticker}</p>
                                    <p style="color: #EF4444; font-size: 0.85rem;">Data unavailable</p>
                                </div>
                                """, unsafe_allow_html=True)

                    st.markdown("---")

                    # ── 2. Portfolio Allocation & Risk Assessment ──
                    tab1, tab2, tab3 = st.tabs(["💼 Portfolio & Risk", "📄 Executive Report", "🤖 Agent Logs"])

                    with tab1:
                        c_alloc, c_risk = st.columns(2)
                        
                        with c_alloc:
                            st.markdown("#### 🎯 AI Portfolio Allocation")
                            allocations = portfolio.get("allocations", {})
                            if allocations and isinstance(allocations, dict):
                                clean_labels = []
                                clean_values = []
                                for k, v in allocations.items():
                                    clean_labels.append(str(k))
                                    clean_values.append(safe_float(v, 0.0))

                                if sum(clean_values) > 0:
                                    fig = px.pie(
                                        values=clean_values,
                                        names=clean_labels,
                                        hole=0.45,
                                        template="plotly_dark",
                                        color_discrete_sequence=px.colors.qualitative.Prism
                                    )
                                    fig.update_layout(
                                        margin=dict(t=20, b=20, l=20, r=20),
                                        paper_bgcolor="rgba(0,0,0,0)",
                                        plot_bgcolor="rgba(0,0,0,0)",
                                        font=dict(family="Plus Jakarta Sans", size=13)
                                    )
                                    st.plotly_chart(fig, use_container_width=True)
                                else:
                                    st.info("Allocation percentages sum to zero.")
                                st.success(f"**Strategy**: {portfolio.get('strategy', 'Balanced asset allocation')}")
                            else:
                                st.info("No allocation data returned.")

                        with c_risk:
                            st.markdown("#### ⚠️ Multi-Factor Risk Assessment")
                            risk_scores = risk.get("risk_scores", {})
                            overall = str(risk.get("overall_risk", "medium")).lower()
                            overall_badge = "🟢 LOW" if "low" in overall else "🟠 MEDIUM" if "med" in overall else "🔴 HIGH"
                            
                            st.markdown(f"**Overall Portfolio Risk Level:** {overall_badge}")
                            if risk.get("recommendation"):
                                st.caption(f"_{risk.get('recommendation')}_")
                            
                            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
                            if isinstance(risk_scores, dict):
                                for ticker, rinfo in risk_scores.items():
                                    if isinstance(rinfo, dict):
                                        score = safe_float(rinfo.get("score"), 5.0)
                                        level = str(rinfo.get("level", "medium")).lower()
                                        col = "green" if "low" in level else "orange" if "med" in level else "red"
                                        progress_val = min(max(score / 10.0, 0.0), 1.0)
                                        
                                        st.markdown(f"**{ticker}** — Risk: :{col}[{level.upper()}] ({int(score)}/10)")
                                        st.progress(progress_val)
                                        if rinfo.get("factors"):
                                            st.caption(f"Factors: {rinfo.get('factors')}")

                    with tab2:
                        st.markdown("#### 📄 Detailed Investment Report")
                        if report:
                            st.markdown(report)
                            st.download_button(
                                label="📥 Download Full Report (Markdown)",
                                data=report,
                                file_name=f"finagent_report_{raw_tickers[0]}.md",
                                mime="text/markdown",
                                use_container_width=True
                            )
                        else:
                            st.info("Report content is being compiled.")

                    with tab3:
                        st.markdown("#### 🤖 LangGraph Pipeline Message Log")
                        for msg in messages:
                            st.code(str(msg), language="text")

                else:
                    # Clean error extraction
                    status_box.update(label="❌ Analysis failed", state="error")
                    err_detail = response.text
                    try:
                        err_json = response.json()
                        err_detail = err_json.get("detail", response.text)
                    except Exception:
                        pass
                    
                    st.error(f"**API Execution Error**: {err_detail}")
                    
                    if "model_not_found" in str(err_detail) or "404" in str(err_detail):
                        st.warning("""
                        **Model Configuration Notice**:
                        The Groq model specified by the server is deprecated or unavailable.
                        - The backend has now been updated with automatic fallback support (`openai/gpt-oss-120b`, `openai/gpt-oss-20b`, `qwen/qwen3.6-27b`).
                        - If you are running on Render or HuggingFace Spaces, redeploy the latest backend code to resolve this issue permanently.
                        """)

            except requests.exceptions.ConnectionError:
                status_box.update(label="⚠️ Connection timeout", state="error")
                st.error("⚠️ **Backend is offline or waking up** (Render free-tier instances spin down after inactivity).")
                st.info("👉 Click **Check Backend Health** in the sidebar, wait 20 seconds, and try clicking **Analyze Stocks** again.")

            except requests.exceptions.Timeout:
                status_box.update(label="⏱️ Request timed out", state="error")
                st.error("⏱️ **Request timed out**. The multi-agent pipeline is processing deep market & news data.")
                st.info("👉 Please retry in a few seconds.")

            except Exception as e:
                status_box.update(label="❌ Unexpected error", state="error")
                st.error(f"**Unexpected error:** {str(e)}")

# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#64748B; font-size:0.85rem; padding: 1rem 0;'>"
    "FinAgent AI • Built with <b>LangGraph</b>, <b>Groq LLM</b>, <b>FastAPI</b> & <b>Streamlit</b> • Educational Purposes Only"
    "</div>",
    unsafe_allow_html=True
)