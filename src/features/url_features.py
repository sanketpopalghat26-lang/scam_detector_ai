"""URL lexical, structural, and typosquatting feature engineering.
Compatible with Scikit-learn pipelines.
"""

import re
import urllib.parse
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from src.features.brand_database import TOP_BRAND_DOMAINS, SUSPICIOUS_TLDS


def levenshtein_distance(s1: str, s2: str) -> int:
    """Compute Levenshtein edit distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def extract_domain_parts(url: str) -> dict:
    """Safely parse URL components."""
    if not isinstance(url, str):
        url = "" if url is None else str(url)

    url_clean = url.strip()
    if not url_clean.startswith(('http://', 'https://', 'ftp://')):
        url_parsed_str = 'http://' + url_clean
    else:
        url_parsed_str = url_clean

    try:
        parsed = urllib.parse.urlparse(url_parsed_str)
        netloc = parsed.netloc.lower()
        path = parsed.path
        query = parsed.query
    except Exception:
        netloc = ""
        path = ""
        query = ""

    # Strip port if present
    host = netloc.split(':')[0] if ':' in netloc else netloc

    # Extract base domain & TLD
    parts = host.split('.')
    if len(parts) >= 2:
        tld = parts[-1]
        base_domain = parts[-2]
        subdomains = parts[:-2]
    else:
        tld = ""
        base_domain = host
        subdomains = []

    return {
        "raw_url": url_clean,
        "host": host,
        "path": path,
        "query": query,
        "tld": tld,
        "base_domain": base_domain,
        "subdomains": subdomains,
        "is_https": 1.0 if url_clean.lower().startswith('https://') else 0.0,
        "has_port": 1.0 if ':' in netloc else 0.0
    }


class URLFeatureExtractor(BaseEstimator, TransformerMixin):
    """Extracts comprehensive lexical, structural, and brand typosquatting features from URLs."""

    def __init__(self):
        # Pre-extract normalized base names from brand database
        self.brand_base_names = [b.split('.')[0].lower() for b in TOP_BRAND_DOMAINS]
        self.feature_names_ = [
            "url_length",
            "host_length",
            "path_length",
            "query_length",
            "dot_count",
            "hyphen_count",
            "underscore_count",
            "slash_count",
            "question_count",
            "at_count",
            "percent_count",
            "digit_count",
            "digit_ratio",
            "subdomain_count",
            "is_ip_host",
            "is_https",
            "has_port",
            "is_suspicious_tld",
            "has_brand_keyword_in_url",
            "min_levenshtein_to_brand",
            "max_brand_similarity_ratio",
            "is_typosquatting_candidate"
        ]

    def fit(self, X, y=None):
        return self

    def _extract_single(self, url: str) -> list:
        parts = extract_domain_parts(url)
        raw = parts["raw_url"]
        host = parts["host"]
        path = parts["path"]
        query = parts["query"]
        tld = parts["tld"]
        base_domain = parts["base_domain"]

        url_len = len(raw)
        host_len = len(host)
        path_len = len(path)
        query_len = len(query)

        # Character counts
        dot_count = raw.count('.')
        hyphen_count = raw.count('-')
        underscore_count = raw.count('_')
        slash_count = raw.count('/')
        question_count = raw.count('?')
        at_count = raw.count('@')
        percent_count = raw.count('%')

        digits = sum(1 for c in raw if c.isdigit())
        digit_ratio = digits / max(url_len, 1)

        subdomain_count = len(parts["subdomains"])

        # Host checks
        is_ip = 1.0 if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', host) else 0.0
        is_https = parts["is_https"]
        has_port = parts["has_port"]
        is_suspicious_tld = 1.0 if tld in SUSPICIOUS_TLDS else 0.0

        # Brand check in raw URL
        has_brand_kw = 1.0 if any(b in raw.lower() for b in self.brand_base_names) else 0.0

        # Typosquatting distance
        min_dist = 999
        max_sim = 0.0
        is_typo = 0.0

        if base_domain and not is_ip:
            for brand in self.brand_base_names:
                dist = levenshtein_distance(base_domain, brand)
                max_len = max(len(base_domain), len(brand))
                sim = 1.0 - (dist / max(max_len, 1))

                if dist < min_dist:
                    min_dist = dist
                if sim > max_sim:
                    max_sim = sim

                # Flag candidate typosquatting if edit distance is 1 or 2 to a brand, but not exact match
                if 0 < dist <= 2 and len(base_domain) >= 4:
                    is_typo = 1.0
        else:
            min_dist = 0
            max_sim = 0.0

        return [
            float(url_len),
            float(host_len),
            float(path_len),
            float(query_len),
            float(dot_count),
            float(hyphen_count),
            float(underscore_count),
            float(slash_count),
            float(question_count),
            float(at_count),
            float(percent_count),
            float(digits),
            float(digit_ratio),
            float(subdomain_count),
            is_ip,
            is_https,
            has_port,
            is_suspicious_tld,
            has_brand_kw,
            float(min_dist),
            float(max_sim),
            is_typo
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

        features = [self._extract_single(url) for url in X_list]
        return np.array(features, dtype=np.float64)

    def get_feature_names_out(self, input_features=None):
        return np.array(self.feature_names_)
