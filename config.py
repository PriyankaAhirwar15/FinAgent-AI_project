import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Groq LLM Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Active Groq Models with fallback cascade
MODEL_NAME = os.getenv("MODEL_NAME", "openai/gpt-oss-120b")
FALLBACK_MODELS = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "qwen/qwen3.6-27b",
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant"
]

def get_llm(model_name: str = None, temperature: float = 0.2):
    """Returns a ChatGroq client instance."""
    model = model_name or MODEL_NAME
    return ChatGroq(api_key=GROQ_API_KEY, model=model, temperature=temperature)

def safe_llm_invoke(prompt: str, preferred_model: str = None, temperature: float = 0.2):
    """
    Invokes Groq LLM with automatic fallback support in case a model is
    deprecated, unavailable, or restricted (e.g., 404 model_not_found).
    """
    active_primary = preferred_model or MODEL_NAME
    models_to_try = [active_primary] + [m for m in FALLBACK_MODELS if m != active_primary]
    last_error = None

    for model in models_to_try:
        try:
            client = ChatGroq(api_key=GROQ_API_KEY, model=model, temperature=temperature)
            return client.invoke(prompt)
        except Exception as e:
            last_error = e
            err_str = str(e).lower()
            if any(term in err_str for term in ["model_not_found", "404", "does not exist", "decommissioned", "invalid_request_error"]):
                continue
            # If it's a rate limit or API key error, re-raise directly
            raise e

    raise last_error

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
