import sqlite3
import os
from config import DATA_DIR, NEWS_DB, MARKET_DB, GTI_DB, PREDICTIONS_DB


def init_all():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs("prediction/models", exist_ok=True)
    _init_news_db()
    _init_market_db()
    _init_gti_db()
    _init_predictions_db()
    print("All databases initialized.")


def _init_news_db():
    conn = sqlite3.connect(NEWS_DB)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS gdelt_events (
            event_id         TEXT PRIMARY KEY,
            timestamp        TEXT,
            actor1_country   TEXT,
            actor2_country   TEXT,
            event_code       TEXT,
            goldstein_scale  REAL,
            num_articles     INTEGER,
            avg_tone         REAL
        );
        CREATE TABLE IF NOT EXISTS rss_articles (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            title            TEXT,
            source           TEXT,
            published_at     TEXT,
            vader_compound   REAL,
            vader_label      TEXT,
            fetched_at       TEXT,
            UNIQUE(title, source)
        );
        CREATE TABLE IF NOT EXISTS newsapi_headlines (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            title            TEXT,
            source           TEXT,
            published_at     TEXT,
            vader_compound   REAL,
            fetched_at       TEXT
        );
    """)
    conn.close()


def _init_market_db():
    conn = sqlite3.connect(MARKET_DB)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS ohlcv (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol    TEXT,
            timestamp TEXT,
            open      REAL,
            high      REAL,
            low       REAL,
            close     REAL,
            volume    REAL,
            UNIQUE(symbol, timestamp)
        );
    """)
    conn.close()


def _init_gti_db():
    conn = sqlite3.connect(GTI_DB)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS gti_scores (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT UNIQUE,
            gti_score   REAL,
            conflict_ct INTEGER,
            avg_tone    REAL,
            vader_avg   REAL
        );
    """)
    conn.close()


def _init_predictions_db():
    conn = sqlite3.connect(PREDICTIONS_DB)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS predictions (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp       TEXT UNIQUE,
            gti_score       REAL,
            vol_prediction  TEXT,
            dir_prediction  TEXT,
            vol_prob        REAL,
            dir_prob        REAL
        );
    """)
    conn.close()


def get_conn(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
