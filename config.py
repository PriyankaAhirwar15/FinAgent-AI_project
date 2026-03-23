import os
from dotenv import load_dotenv
load_dotenv()
# Groq LLM Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
MODEL_NAME = "llama-3.3-70b-versatile"
# Tavily Search Configuration
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
# App Configuration
APP_NAME = "FinAgent AI"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "6-Agent Stock Market Analyzer"
# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
# Report Configuration
REPORTS_DIR = "reports/generated"
# Agent Configuration
MAX_RETRIES = 3
RECURSION_LIMIT = 25
