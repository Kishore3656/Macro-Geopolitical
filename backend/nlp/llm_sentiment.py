"""
LLM Sentiment Analysis
======================
Provider abstraction for multi-LLM support: Ollama, HuggingFace, and fallback VADER.

Analyzes headlines for sentiment, geopolitical regime, and generates narratives.
All providers are optional; system gracefully degrades to VADER if LLM unavailable.

Cost:
  - Ollama: $0 (local)
  - HuggingFace free tier: $0 (30k req/month)
  - VADER: $0 (built-in NLTK)
"""

import os
import json
import time
import hashlib
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from dataclasses import dataclass
from collections import deque, Counter
import requests

from config import (
    USE_LLM_SENTIMENT,
    LLM_PROVIDER,
    OLLAMA_API_URL,
    OLLAMA_MODEL,
    HUGGINGFACE_API_KEY,
    LLM_CACHE_TTL_MINS,
)

try:
    from nlp.ner import EntityExtractor
    NER_AVAILABLE = True
except ImportError:
    NER_AVAILABLE = False

try:
    from nlp.language import LanguageProcessor
    LANGUAGE_PROCESSOR_AVAILABLE = True
except ImportError:
    LANGUAGE_PROCESSOR_AVAILABLE = False


@dataclass
class LLMAnalysis:
    """Structured output from sentiment analysis."""
    sentiment_score: float  # -1.0 to 1.0
    regime: str  # "risk-on", "risk-off", "crisis", "neutral"
    entities: list[str]  # ["Ukraine", "Oil", "Fed"]
    narrative: str  # English explanation
    provider_used: str  # "ollama", "huggingface", "vader"
    confidence: float = 0.5  # 0.0-1.0 consensus confidence on regime
    cached: bool = False


class LLMProvider(ABC):
    """Abstract base for LLM providers."""

    @abstractmethod
    def analyze(self, headlines: list[str]) -> LLMAnalysis:
        """Analyze headlines and return structured LLMAnalysis."""
        pass


class OllamaProvider(LLMProvider):
    """Local Ollama LLM provider."""

    def __init__(self, api_url: str = OLLAMA_API_URL, model: str = OLLAMA_MODEL):
        self.api_url = api_url
        self.model = model
        self.timeout = 10

    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API and return response text."""
        try:
            response = requests.post(
                f"{self.api_url}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            raise RuntimeError(f"Ollama API error: {e}")

    def analyze(self, headlines: list[str]) -> LLMAnalysis:
        """Analyze headlines using Ollama."""
        headlines_text = "\n".join(f"- {h}" for h in headlines[:10])

        prompt = f"""Analyze these geopolitical and market headlines for sentiment and regime.

Headlines:
{headlines_text}

Respond with ONLY valid JSON, no other text:
{{
  "sentiment_score": <number -1.0 to 1.0>,
  "regime": "<risk-on|risk-off|crisis|neutral>",
  "entities": [<list of key entities mentioned>],
  "narrative": "<1-sentence explanation of regime>"
}}"""

        try:
            response_text = self._call_ollama(prompt)
            response_text = response_text.strip()

            # Extract JSON if model wrapped it in markdown
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            data = json.loads(response_text)
            return LLMAnalysis(
                sentiment_score=float(data.get("sentiment_score", 0.0)),
                regime=str(data.get("regime", "neutral")).lower(),
                entities=data.get("entities", []),
                narrative=str(data.get("narrative", "")),
                provider_used="ollama",
                cached=False,
            )
        except Exception as e:
            raise RuntimeError(f"Ollama analysis failed: {e}")


class HuggingFaceProvider(LLMProvider):
    """HuggingFace free-tier provider (30k requests/month limit)."""

    def __init__(self, api_key: str = HUGGINGFACE_API_KEY):
        self.api_key = api_key
        self.timeout = 10

    def analyze(self, headlines: list[str]) -> LLMAnalysis:
        """Analyze using HuggingFace inference API."""
        if not self.api_key:
            raise RuntimeError("HUGGINGFACE_API_KEY not set")

        # Sentiment analysis via distilbert
        headlines_text = " ".join(headlines[:10])
        headers = {"Authorization": f"Bearer {self.api_key}"}

        try:
            # Sentiment
            sent_response = requests.post(
                "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english",
                json={"inputs": headlines_text},
                headers=headers,
                timeout=self.timeout,
            )
            sent_response.raise_for_status()
            sent_data = sent_response.json()[0]
            sentiment_score = (
                sent_data["score"] if sent_data["label"] == "POSITIVE" else -sent_data["score"]
            )

            # Zero-shot regime classification
            regime_response = requests.post(
                "https://api-inference.huggingface.co/models/facebook/bart-large-mnli",
                json={
                    "inputs": headlines_text,
                    "parameters": {"candidate_labels": ["risk-on", "risk-off", "crisis", "neutral"]},
                },
                headers=headers,
                timeout=self.timeout,
            )
            regime_response.raise_for_status()
            regime_data = regime_response.json()
            regime = regime_data["labels"][0]  # Top candidate

            return LLMAnalysis(
                sentiment_score=float(sentiment_score),
                regime=regime,
                entities=[],  # Would need NER model, skip for now
                narrative=f"Markets showing {regime} sentiment based on headline analysis.",
                provider_used="huggingface",
                cached=False,
            )
        except Exception as e:
            raise RuntimeError(f"HuggingFace analysis failed: {e}")


class NullProvider(LLMProvider):
    """VADER-only fallback. No LLM calls."""

    def analyze(self, headlines: list[str]) -> LLMAnalysis:
        """Analyze using VADER sentiment only."""
        try:
            from nltk.sentiment import SentimentIntensityAnalyzer
            import nltk

            try:
                nltk.data.find("vader_lexicon")
            except LookupError:
                nltk.download("vader_lexicon", quiet=True)

            sia = SentimentIntensityAnalyzer()
            headlines_text = " ".join(headlines[:10])
            scores = sia.polarity_scores(headlines_text)
            sentiment_score = scores["compound"]

            if sentiment_score > 0.2:
                regime = "risk-on"
            elif sentiment_score < -0.2:
                regime = "risk-off"
            elif sentiment_score < -0.5:
                regime = "crisis"
            else:
                regime = "neutral"

            return LLMAnalysis(
                sentiment_score=sentiment_score,
                regime=regime,
                entities=[],
                narrative=f"VADER sentiment score: {sentiment_score:.3f} — regime: {regime}",
                provider_used="vader",
                cached=False,
            )
        except Exception as e:
            raise RuntimeError(f"VADER analysis failed: {e}")


class AnalysisCache:
    """In-memory cache with TTL for LLM analysis."""

    def __init__(self, ttl_mins: int = LLM_CACHE_TTL_MINS):
        self.ttl = ttl_mins * 60  # Convert to seconds
        self.cache = {}  # key -> (value, timestamp)

    def get(self, headlines_hash: str) -> LLMAnalysis | None:
        """Retrieve from cache if not expired."""
        if headlines_hash in self.cache:
            value, timestamp = self.cache[headlines_hash]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                del self.cache[headlines_hash]
        return None

    def set(self, headlines_hash: str, analysis: LLMAnalysis):
        """Store in cache."""
        self.cache[headlines_hash] = (analysis, time.time())

    def clear_expired(self):
        """Remove expired entries."""
        now = time.time()
        expired = [k for k, (_, ts) in self.cache.items() if now - ts >= self.ttl]
        for k in expired:
            del self.cache[k]


class RateLimiter:
    """Token bucket rate limiter (in-memory)."""

    def __init__(self, rpm: int = 60):
        self.rpm = rpm
        self.tokens = deque()

    def allow(self) -> bool:
        """Check if request is allowed under rate limit."""
        now = time.time()
        minute_ago = now - 60

        # Remove tokens older than 1 minute
        while self.tokens and self.tokens[0] < minute_ago:
            self.tokens.popleft()

        # Allow if under limit
        if len(self.tokens) < self.rpm:
            self.tokens.append(now)
            return True
        return False


# Global instances
_cache = AnalysisCache()
_rate_limiter = RateLimiter(rpm=60)
_regime_history = deque(maxlen=10)  # Track last 10 regimes for confidence scoring
_entity_extractor = EntityExtractor() if NER_AVAILABLE else None
_language_processor = LanguageProcessor() if LANGUAGE_PROCESSOR_AVAILABLE else None


def _get_provider() -> LLMProvider:
    """Select LLM provider based on config."""
    if not USE_LLM_SENTIMENT or LLM_PROVIDER == "none":
        return NullProvider()

    if LLM_PROVIDER == "ollama":
        return OllamaProvider()
    elif LLM_PROVIDER == "huggingface":
        return HuggingFaceProvider()
    else:
        # Default fallback
        return NullProvider()


def _calculate_regime_confidence(regime: str) -> float:
    """
    Calculate confidence in regime prediction based on recent regime history.
    If 8/10 recent regimes match current → confidence = 0.8
    """
    _regime_history.append(regime)

    if len(_regime_history) < 2:
        return 0.5

    regime_counts = Counter(_regime_history)
    consensus_count = regime_counts[regime]
    confidence = consensus_count / len(_regime_history)

    return confidence


def _extract_entities_from_headlines(headlines: list[str]) -> list[str]:
    """Extract top entities from headlines using NER if available."""
    if not _entity_extractor or not NER_AVAILABLE:
        return []

    try:
        return _entity_extractor.extract_top_entities(headlines, limit=5)
    except Exception as e:
        print(f"Entity extraction error: {e}")
        return []


def _process_multilingual_headlines(headlines: list[str]) -> list[str]:
    """Detect language and translate non-English headlines if processor available."""
    if not _language_processor or not LANGUAGE_PROCESSOR_AVAILABLE:
        return headlines

    processed = []
    for headline in headlines:
        try:
            _, english_text, _ = _language_processor.process_headline(headline)
            processed.append(english_text)
        except Exception as e:
            print(f"Language processing error: {e}")
            processed.append(headline)

    return processed


def get_llm_analysis(headlines: list[str]) -> LLMAnalysis:
    """
    Analyze headlines for sentiment, regime, and narrative.

    Returns LLMAnalysis with sentiment_score, regime, entities, narrative, confidence.
    Falls back gracefully: LLM → cache → VADER → error handling.

    Parameters
    ----------
    headlines : list[str]
        List of headline texts (up to 10 used)

    Returns
    -------
    LLMAnalysis
        Structured analysis with regime, confidence, entities, and narrative
    """
    if not headlines:
        return LLMAnalysis(
            sentiment_score=0.0,
            regime="neutral",
            entities=[],
            narrative="No headlines provided.",
            provider_used="null",
            confidence=0.5,
        )

    # Process multi-language headlines
    headlines_processed = _process_multilingual_headlines(headlines)

    # Hash headlines for cache key
    headlines_key = hashlib.md5("|".join(headlines_processed[:10]).encode()).hexdigest()

    # Check cache
    cached = _cache.get(headlines_key)
    if cached:
        cached.cached = True
        return cached

    # Check rate limit
    if not _rate_limiter.allow():
        # If rate-limited, fall back to VADER
        null_provider = NullProvider()
        try:
            analysis = null_provider.analyze(headlines_processed)
            analysis.narrative += " (RATE LIMITED — VADER fallback)"
            analysis.confidence = _calculate_regime_confidence(analysis.regime)
            # Extract entities from headlines
            if not analysis.entities:
                analysis.entities = _extract_entities_from_headlines(headlines_processed)
            _cache.set(headlines_key, analysis)
            return analysis
        except Exception:
            return LLMAnalysis(
                sentiment_score=0.0,
                regime="neutral",
                entities=[],
                narrative="Analysis unavailable (rate limit).",
                provider_used="error",
                confidence=0.5,
            )

    # Try primary provider
    provider = _get_provider()
    try:
        analysis = provider.analyze(headlines_processed)
        analysis.confidence = _calculate_regime_confidence(analysis.regime)
        # Extract entities if not already populated
        if not analysis.entities:
            analysis.entities = _extract_entities_from_headlines(headlines_processed)
        _cache.set(headlines_key, analysis)
        return analysis
    except Exception as e:
        # Fallback to VADER on any LLM error
        try:
            null_provider = NullProvider()
            analysis = null_provider.analyze(headlines_processed)
            analysis.narrative += f" (LLM unavailable: {provider.__class__.__name__} — VADER fallback)"
            analysis.confidence = _calculate_regime_confidence(analysis.regime)
            if not analysis.entities:
                analysis.entities = _extract_entities_from_headlines(headlines_processed)
            _cache.set(headlines_key, analysis)
            return analysis
        except Exception as fallback_err:
            # Final fallback: return neutral analysis
            return LLMAnalysis(
                sentiment_score=0.0,
                regime="neutral",
                entities=[],
                narrative=f"Analysis unavailable ({str(e)}). Using neutral regime.",
                provider_used="error",
                confidence=0.5,
            )


if __name__ == "__main__":
    # Test
    import json

    test_headlines = [
        "Ukraine reports major military advances amid supply concerns",
        "Fed signals potential rate cut next quarter",
        "Oil prices spike on geopolitical tensions",
        "Tech stocks rally on AI enthusiasm",
        "Gold hits 6-month high as investors flee risk",
    ]

    result = get_llm_analysis(test_headlines)
    print(json.dumps(
        {
            "sentiment_score": result.sentiment_score,
            "regime": result.regime,
            "entities": result.entities,
            "narrative": result.narrative,
            "provider_used": result.provider_used,
            "cached": result.cached,
        },
        indent=2,
    ))
