<div align="center">
# 💰 FinAgent AI
### Production-Grade 6-Agent Stock Market Analyzer
<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=22&pause=1000&color=00D4FF&center=true&vCenter=true&width=600&lines=6+Specialized+AI+Agents;Live+Stock+Market+Data;Portfolio+Optimization;Risk+Assessment;Investment+Reports" alt="Typing SVG" />
---
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-00D4FF?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-LLaMA3.3-FF6B35?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Deployed-FFD21E?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
---
[Live Demo](https://huggingface.co/spaces/yourusername/finagent-ai) •
[API Docs](http://localhost:8000/docs) •
[Report Bug](https://github.com/yourusername/FinAgent-AI/issues)
</div>
---
## What Is FinAgent AI?
FinAgent AI is a production-grade multi-agent stock market analyzer. It uses 6 specialized AI agents working together in a LangGraph pipeline to deliver comprehensive investment analysis, portfolio optimization, and risk assessment — all powered by live market data and Groq LLaMA 3.3-70B.
---
## System Architecture
\\\
╔══════════════════════════════════════════════════════════╗
║                    FinAgent AI System                    ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║   User Input (Streamlit UI)                              ║
║         │                                                ║
║         ▼                                                ║
║   FastAPI Backend  ──────────────────────────────────    ║
║         │                                                ║
║         ▼                                                ║
║   LangGraph Pipeline                                     ║
║         │                                                ║
║    ┌────▼────┐                                           ║
║    │Agent 1  │  Supervisor                               ║
║    │         │  Orchestrates all agents                  ║
║    └────┬────┘                                           ║
║         │                                                ║
║    ┌────▼────┐                                           ║
║    │Agent 2  │  Market Researcher                        ║
║    │         │  Live stock data via yFinance             ║
║    └────┬────┘                                           ║
║         │                                                ║
║    ┌────▼────┐                                           ║
║    │Agent 3  │  News Analyzer                            ║
║    │         │  Sentiment analysis via Tavily            ║
║    └────┬────┘                                           ║
║         │                                                ║
║    ┌────▼────┐                                           ║
║    │Agent 4  │  Portfolio Optimizer                      ║
║    │         │  AI-powered allocation strategy           ║
║    └────┬────┘                                           ║
║         │                                                ║
║    ┌────▼────┐                                           ║
║    │Agent 5  │  Risk Assessor                            ║
║    │         │  Risk scoring and analysis                ║
║    └────┬────┘                                           ║
║         │                                                ║
║    ┌────▼────┐                                           ║
║    │Agent 6  │  Report Generator                         ║
║    │         │  Professional investment report           ║
║    └────┬────┘                                           ║
║         │                                                ║
║         ▼                                                ║
║   Beautiful Results + PDF Report                         ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
\\\
---
## Agent Pipeline Flow
\\\mermaid
graph TD
    A[User Input] --> B[FastAPI Backend]
    B --> C{Supervisor Agent}
    C --> D[Market Researcher]
    D --> |Live Stock Data| E[News Analyzer]
    E --> |Sentiment Scores| F[Portfolio Optimizer]
    F --> |Allocation Strategy| G[Risk Assessor]
    G --> |Risk Scores| H[Report Generator]
    H --> I[Investment Report]
    I --> J[Streamlit Dashboard]
    style A fill:#00D4FF,color:#000
    style C fill:#FF6B35,color:#fff
    style I fill:#00FF88,color:#000
    style J fill:#FF4B4B,color:#fff
\\\
---
## How It Beats Traditional Stock Analyzers
| Feature | Traditional App | FinAgent AI |
|---|---|---|
| Analysis Type | Single model | 6 specialized agents |
| Data Source | Static/delayed | Live real-time data |
| News Analysis | None | AI sentiment scoring |
| Portfolio | Manual | AI-optimized |
| Risk Assessment | Basic | Multi-factor AI |
| Report | None | Full PDF report |
| Self-Correction | None | Automatic retry |
| Deployment | Local only | Cloud + Docker |
---
## Tech Stack
\\\
Frontend    │ Streamlit
Backend     │ FastAPI + Uvicorn
Agents      │ LangGraph + LangChain
LLM         │ Groq LLaMA 3.3-70B
Stock Data  │ yFinance (FREE)
News Search │ Tavily API (FREE)
Charts      │ Plotly
Container   │ Docker + Docker Compose
Deployment  │ HuggingFace Spaces
Version     │ Git + GitHub
\\\
---
## Quick Start
### Prerequisites
- Python 3.10+
- Groq API Key (free at console.groq.com)
- Tavily API Key (free at app.tavily.com)
### Installation
\\\ash
# Clone the repository
git clone https://github.com/yourusername/FinAgent-AI.git
cd FinAgent-AI
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# Install dependencies
pip install -r requirements.txt
# Set up environment variables
cp .env.example .env
# Add your API keys to .env file
\\\
### Running The App
\\\ash
# Terminal 1 - Start FastAPI backend
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
# Terminal 2 - Start Streamlit frontend
streamlit run frontend/app.py
\\\
### Docker Deployment
\\\ash
docker-compose -f docker/docker-compose.yml up --build
\\\
---
## API Endpoints
| Method | Endpoint | Description |
|---|---|---|
| GET | / | Root endpoint |
| GET | /health | Health check |
| POST | /analyze | Analyze stocks |
| GET | /docs | API documentation |
### Example API Request
\\\python
import requests
response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "query": "Best stocks for long term investment",
        "stocks": ["AAPL", "TSLA", "GOOGL"]
    }
)
print(response.json())
\\\
---
## Project Structure
\\\
FinAgent-AI/
│
├── agents/
│   ├── supervisor.py          # Task orchestration
│   ├── market_researcher.py   # Live stock data
│   ├── news_analyzer.py       # News sentiment
│   ├── portfolio_optimizer.py # Portfolio strategy
│   ├── risk_assessor.py       # Risk scoring
│   └── report_generator.py    # Report creation
│
├── core/
│   ├── state.py               # Shared agent state
│   ├── graph.py               # LangGraph pipeline
│   └── checkpointer.py        # Memory persistence
│
├── tools/
│   ├── stock_tool.py          # yFinance wrapper
│   ├── news_tool.py           # Tavily wrapper
│   └── chart_tool.py          # Plotly charts
│
├── api/
│   └── main.py                # FastAPI backend
│
├── frontend/
│   └── app.py                 # Streamlit dashboard
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── reports/generated/         # AI generated reports
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
\\\
---
## Results Sample
\\\
Stock Analysis: AAPL, TSLA, GOOGL
Overall Risk: LOW
Portfolio Strategy: Growth-focused allocation
AAPL  → 45% allocation │ Risk: LOW    │ Sentiment: POSITIVE
TSLA  → 25% allocation │ Risk: HIGH   │ Sentiment: NEUTRAL
GOOGL → 30% allocation │ Risk: LOW    │ Sentiment: POSITIVE
\\\
---
## License
MIT License - Copyright 2026 Priyanka Ashok Ahirwar
---
<div align="center">
### Built with by Priyanka Ashok Ahirwar
![Visitors](https://visitor-badge.laobi.icu/badge?page_id=yourusername.FinAgent-AI)
*This project is for educational purposes only. Not financial advice.*
</div>
