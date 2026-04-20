from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from core.graph import graph
import uvicorn
import os

app = FastAPI(
    title="FinAgent AI",
    description="6-Agent Stock Market Analyzer",
    version="1.0.0"
)

# Allow all origins so Streamlit frontend can talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalysisRequest(BaseModel):
    query: str
    stocks: List[str]


class AnalysisResponse(BaseModel):
    success: bool
    report: str
    market_data: dict
    portfolio_allocation: dict
    risk_assessment: dict
    messages: List[str]


@app.get("/")
def root():
    # Root endpoint for basic API info
    return {
        "app": "FinAgent AI",
        "version": "1.0.0",
        "status": "running",
        "agents": 6
    }


@app.get("/health")
def health():
    # Health check endpoint — used by cron-job and Docker healthcheck
    return {"status": "healthy"}


@app.post("/analyze", response_model=AnalysisResponse)
def analyze_stocks(request: AnalysisRequest):
    try:
        if not request.stocks:
            raise HTTPException(status_code=400, detail="No stocks provided")

        # Clean and uppercase all tickers
        stocks = [s.upper().strip() for s in request.stocks]

        # Run the LangGraph agent pipeline
        result = graph.invoke({
            "query": request.query,
            "stocks": stocks,
            "messages": [],
            "market_data": {},
            "news_sentiment": {},
            "portfolio_allocation": {},
            "risk_assessment": {},
            "final_report": "",
            "current_agent": "",
            "error": "",
            "retry_count": 0,
            "next_step": ""
        })

        return AnalysisResponse(
            success=True,
            report=result.get("final_report", ""),
            market_data=result.get("market_data", {}),
            portfolio_allocation=result.get("portfolio_allocation", {}),
            risk_assessment=result.get("risk_assessment", {}),
            messages=result.get("messages", [])
        )

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise

    except Exception as e:
        # Catch all other errors and return 500
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    port = int(os.environ.get("API_PORT", 8000))
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=port,
        reload=False  # Always False in production
    )