"""
VADER sentiment scorer — CPU-only, runs in microseconds per headline.
Returns compound score and label for any text string.
"""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from config import VADER_COMPOUND_THRESHOLD

_analyzer = SentimentIntensityAnalyzer()


def score_headline(text: str) -> dict:
    """
    Score a single headline.
    Returns: {"compound": float, "label": "positive"|"negative"|"neutral"}
    """
    scores = _analyzer.polarity_scores(text)
    compound = scores["compound"]
    if compound <= VADER_COMPOUND_THRESHOLD:
        label = "negative"
    elif compound >= abs(VADER_COMPOUND_THRESHOLD):
        label = "positive"
    else:
        label = "neutral"
    return {"compound": round(compound, 4), "label": label}


def score_batch(texts: list) -> list:
    """Score a list of headlines. Returns list of dicts."""
    return [score_headline(t) for t in texts]
