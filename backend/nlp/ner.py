"""
Named Entity Recognition (NER) for financial headlines.
Extracts companies, stocks, commodities, and geopolitical entities.
"""

import re
from typing import Dict, List
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("WARNING: spaCy model en_core_web_sm not found. Install with: python -m spacy download en_core_web_sm")
    nlp = None


STOCK_TICKER_PATTERN = r'\b([A-Z]{1,5})\b'
COMMODITY_KEYWORDS = ['oil', 'gold', 'copper', 'wheat', 'bitcoin', 'ethereum', 'natural gas', 'silver', 'lithium']
CURRENCY_KEYWORDS = ['dollar', 'euro', 'yen', 'pound', 'yuan', 'rupee', 'peso']


class EntityExtractor:
    """Extract financial entities from headlines using spaCy + regex patterns."""

    def __init__(self):
        self.nlp = nlp

    def extract_entities(self, text: str) -> List[str]:
        """
        Extract named entities from headline.
        Returns: list of entity names (e.g., ['Apple', 'SEC', 'China'])
        """
        if not self.nlp:
            return []

        doc = self.nlp(text)
        entities = []

        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PERSON', 'GPE', 'PRODUCT']:
                if len(ent.text.split()) <= 3:
                    entities.append(ent.text)

        return list(dict.fromkeys(entities))[:5]

    def extract_financial_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Categorized extraction: stocks, commodities, countries, companies.
        Returns: dict with keys ['stocks', 'commodities', 'countries', 'companies']
        """
        result = {
            'stocks': [],
            'commodities': [],
            'countries': [],
            'companies': [],
        }

        if not self.nlp:
            return result

        doc = self.nlp(text)
        text_lower = text.lower()

        for ent in doc.ents:
            if ent.label_ == 'ORG':
                result['companies'].append(ent.text)
            elif ent.label_ == 'GPE':
                result['countries'].append(ent.text)

        for keyword in COMMODITY_KEYWORDS:
            if keyword in text_lower:
                result['commodities'].append(keyword.title())

        for keyword in CURRENCY_KEYWORDS:
            if keyword in text_lower:
                result['commodities'].append(keyword.title())

        for match in re.findall(STOCK_TICKER_PATTERN, text):
            if 1 < len(match) <= 5 and match.isupper():
                if match not in result['stocks']:
                    result['stocks'].append(match)

        return {k: list(dict.fromkeys(v))[:5] for k, v in result.items()}

    def extract_top_entities(self, headlines: List[str], limit: int = 5) -> List[str]:
        """
        Extract and rank entities across multiple headlines.
        Returns: top N most frequent entities
        """
        from collections import Counter

        all_entities = []
        for headline in headlines:
            all_entities.extend(self.extract_entities(headline))

        if not all_entities:
            return []

        counter = Counter(all_entities)
        return [entity for entity, _ in counter.most_common(limit)]


if __name__ == "__main__":
    extractor = EntityExtractor()

    test_headlines = [
        "Apple and Microsoft report record earnings amid inflation",
        "Oil prices surge as OPEC cuts production, energy stocks rally",
        "China imposes tariffs on US tech exports, Tesla stock drops",
        "Federal Reserve raises rates, gold climbs as safe haven",
    ]

    for headline in test_headlines:
        entities = extractor.extract_entities(headline)
        fin_entities = extractor.extract_financial_entities(headline)
        print(f"Headline: {headline}")
        print(f"  Entities: {entities}")
        print(f"  Financial: {fin_entities}")
        print()

    top_entities = extractor.extract_top_entities(test_headlines)
    print(f"Top entities across headlines: {top_entities}")
