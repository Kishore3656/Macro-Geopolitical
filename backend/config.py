import os
from dotenv import load_dotenv

load_dotenv()

# API keys
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")

# Polling intervals (minutes)
GDELT_POLL_MINS   = 15
RSS_POLL_MINS     = 5
NEWSAPI_POLL_MINS = 15
MARKET_POLL_MINS  = 15

# NLP
VADER_COMPOUND_THRESHOLD = -0.05  # below this = negative sentiment

# LLM Sentiment Analysis (Phase 3)
USE_LLM_SENTIMENT = os.getenv("USE_LLM_SENTIMENT", "false").lower() == "true"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "none")  # "ollama" | "huggingface" | "none"
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
LLM_CACHE_TTL_MINS = int(os.getenv("LLM_CACHE_TTL_MINS", "15"))
LLM_RATE_LIMIT_RPM = int(os.getenv("LLM_RATE_LIMIT_RPM", "60"))

# GTI
GTI_WINDOW_HOURS       = 6
GTI_CONFLICT_THRESHOLD = -5.0    # GoldsteinScale below this = conflict

# Database paths
BACKEND_DIR    = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR    = os.path.dirname(BACKEND_DIR)
DATA_DIR       = os.path.join(PROJECT_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
NEWS_DB        = os.path.join(DATA_DIR, "news.db")
MARKET_DB      = os.path.join(DATA_DIR, "market.db")
GTI_DB         = os.path.join(DATA_DIR, "gti.db")
PREDICTIONS_DB = os.path.join(DATA_DIR, "predictions.db")
NEWSAPI_CALLS  = os.path.join(DATA_DIR, "newsapi_calls.json")

# Model paths
MODELS_DIR     = os.path.join(BACKEND_DIR, "prediction", "models")
os.makedirs(MODELS_DIR, exist_ok=True)
LGBM_VOL_PATH  = os.path.join(MODELS_DIR, "lgbm_volatility.pkl")
LGBM_DIR_PATH  = os.path.join(MODELS_DIR, "lgbm_direction.pkl")

# Market symbols
SYMBOLS = ["SPY", "VIX", "GLD", "CL=F", "EURUSD=X"]

# RSS feeds
RSS_FEEDS = [
    "https://feeds.reuters.com/reuters/worldNews",
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://feeds.feedburner.com/APWorldNews",
]

# NewsAPI daily request guard (stop at 95 to leave buffer)
NEWSAPI_DAILY_LIMIT = 95

# SQLite row fetch limit (RAM guard)
MAX_ROWS = 2000
