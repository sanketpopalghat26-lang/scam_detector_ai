"""Handcrafted text feature engineering for SMS and Email scam detection.
Compatible with Scikit-learn pipelines.
"""

import re
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from src.features.brand_database import (
    URGENCY_KEYWORDS,
    INDUCEMENT_KEYWORDS,
    HIGH_RISK_BRAND_KEYWORDS
)

URL_REGEX = re.compile(
    r'(?:https?://|www\.)[^\s<>"]+|bit\.ly/[^\s<>"]+|tinyurl\.com/[^\s<>"]+|t\.co/[^\s<>"]+',
    re.IGNORECASE
)
PHONE_REGEX = re.compile(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\b\d{5,6}\b')
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')


class HandcraftedTextFeatures(BaseEstimator, TransformerMixin):
    """Extracts structural, lexical, urgency, and brand spoofing signals from text."""

    def __init__(self):
        self.feature_names_ = [
            "char_length",
            "word_count",
            "caps_ratio",
            "digit_ratio",
            "exclamation_count",
            "question_count",
            "dollar_count",
            "url_count",
            "has_url",
            "phone_count",
            "has_phone",
            "urgency_score",
            "inducement_score",
            "brand_mention_count",
            "has_ip_in_text"
        ]

    def fit(self, X, y=None):
        return self

    def _extract_single(self, text: str) -> list:
        if not isinstance(text, str):
            text = "" if text is None else str(text)

        char_len = len(text)
        words = text.split()
        word_count = len(words)
        text_lower = text.lower()

        # Ratio calculations
        caps_count = sum(1 for c in text if c.isupper())
        caps_ratio = caps_count / max(char_len, 1)

        digits = sum(1 for c in text if c.isdigit())
        digit_ratio = digits / max(char_len, 1)

        # Punctuation counts
        exclamation_count = text.count("!")
        question_count = text.count("?")
        dollar_count = text.count("$") + text.count("£") + text.count("€")

        # URLs & Contacts
        urls = URL_REGEX.findall(text)
        url_count = len(urls)
        has_url = 1.0 if url_count > 0 else 0.0

        phones = PHONE_REGEX.findall(text)
        phone_count = len(phones)
        has_phone = 1.0 if phone_count > 0 else 0.0

        # Pattern scores
        urgency_score = sum(1.0 for kw in URGENCY_KEYWORDS if kw in text_lower)
        inducement_score = sum(1.0 for kw in INDUCEMENT_KEYWORDS if kw in text_lower)
        brand_count = sum(1.0 for b in HIGH_RISK_BRAND_KEYWORDS if b in text_lower)

        has_ip = 1.0 if re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', text) else 0.0

        return [
            float(char_len),
            float(word_count),
            float(caps_ratio),
            float(digit_ratio),
            float(exclamation_count),
            float(question_count),
            float(dollar_count),
            float(url_count),
            has_url,
            float(phone_count),
            has_phone,
            urgency_score,
            inducement_score,
            brand_count,
            has_ip
        ]

    def transform(self, X):
        if isinstance(X, pd.Series):
            X_list = X.tolist()
        elif isinstance(X, pd.DataFrame):
            X_list = X.iloc[:, 0].tolist()
        elif isinstance(X, (list, tuple, np.ndarray)):
            X_list = list(X)
        else:
            X_list = [str(X)]

        features = [self._extract_single(text) for text in X_list]
        return np.array(features, dtype=np.float64)

    def get_feature_names_out(self, input_features=None):
        return np.array(self.feature_names_)
