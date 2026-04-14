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

# GTI
GTI_WINDOW_HOURS       = 6
GTI_CONFLICT_THRESHOLD = -5.0    # GoldsteinScale below this = conflict

# Database paths
DATA_DIR       = "data"
NEWS_DB        = "data/news.db"
MARKET_DB      = "data/market.db"
GTI_DB         = "data/gti.db"
PREDICTIONS_DB = "data/predictions.db"
NEWSAPI_CALLS  = "data/newsapi_calls.json"

# Model paths
LGBM_VOL_PATH = "prediction/models/lgbm_volatility.pkl"
LGBM_DIR_PATH = "prediction/models/lgbm_direction.pkl"

# Market symbols
SYMBOLS = ["SPY", "VIX", "GLD"]

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
MAX_ROWS = 500
