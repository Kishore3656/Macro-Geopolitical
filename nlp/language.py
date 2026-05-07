"""
Language detection and translation for multi-language headline analysis.
Detects language and auto-translates non-English headlines to English.
"""

from typing import Tuple
import os

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    print("WARNING: textblob not installed. Language detection will be unavailable.")

try:
    from google.cloud import translate_v2
    GOOGLE_TRANSLATE_AVAILABLE = True
except ImportError:
    GOOGLE_TRANSLATE_AVAILABLE = False

try:
    from googletrans import Translator
    GOOGLETRANS_AVAILABLE = True
except ImportError:
    GOOGLETRANS_AVAILABLE = False


SUPPORTED_LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'zh': 'Chinese',
    'ja': 'Japanese',
    'ru': 'Russian',
    'ar': 'Arabic',
    'pt': 'Portuguese',
    'ko': 'Korean',
}


class LanguageProcessor:
    """Detect language and translate headlines to English."""

    def __init__(self):
        self.textblob_available = TEXTBLOB_AVAILABLE
        self.googletrans_available = GOOGLETRANS_AVAILABLE
        self.google_cloud_available = GOOGLE_TRANSLATE_AVAILABLE

        if self.googletrans_available:
            self.translator = Translator()

    def detect_language(self, text: str) -> str:
        """
        Detect language of text.
        Returns: language code (e.g., 'en', 'es', 'fr')
        Fallback: 'en' if detection unavailable
        """
        if not self.textblob_available:
            return 'en'

        try:
            blob = TextBlob(text)
            lang_code = blob.detect_language()
            return lang_code if lang_code in SUPPORTED_LANGUAGES else 'en'
        except Exception as e:
            print(f"Language detection error: {e}")
            return 'en'

    def translate_to_english(self, text: str, source_lang: str = None) -> Tuple[str, bool]:
        """
        Translate text to English if not already English.
        Returns: (translated_text, was_translated: bool)
        """
        if not source_lang:
            source_lang = self.detect_language(text)

        if source_lang == 'en':
            return text, False

        if self.googletrans_available:
            try:
                result = self.translator.translate(text, src_language=source_lang, dest_language='en')
                return result.get('translatedText', text), True
            except Exception as e:
                print(f"Translation error: {e}")
                return text, False

        if self.google_cloud_available:
            try:
                translate_client = translate_v2.Client()
                result = translate_client.translate_text(
                    text,
                    source_language=source_lang,
                    target_language='en'
                )
                return result['translatedText'], True
            except Exception as e:
                print(f"Google Cloud translation error: {e}")
                return text, False

        print(f"WARNING: No translation library available. Returning original text in {source_lang}")
        return text, False

    def process_headline(self, text: str) -> Tuple[str, str, bool]:
        """
        Detect language, translate if needed, and return both versions.
        Returns: (original_text, english_text, was_translated: bool)
        """
        lang = self.detect_language(text)
        if lang == 'en':
            return text, text, False

        english_text, was_translated = self.translate_to_english(text, lang)
        return text, english_text, was_translated


if __name__ == "__main__":
    processor = LanguageProcessor()

    test_headlines = [
        "Apple reports record earnings",  # English
        "La Bolsa de Madrid sube tras datos de inflacion",  # Spanish
        "La Banque Centrale Europeenne releve les taux",  # French
        "中央银行提高利率应对通胀",  # Chinese
    ]

    for headline in test_headlines:
        lang = processor.detect_language(headline)
        original, english, translated = processor.process_headline(headline)
        print(f"Original ({lang}): {original}")
        print(f"English: {english}")
        print(f"Translated: {translated}")
        print()
