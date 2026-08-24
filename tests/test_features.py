"""Unit tests for text and URL feature extraction pipelines."""

import pytest
import numpy as np
from src.features.text_features import HandcraftedTextFeatures
from src.features.url_features import URLFeatureExtractor, levenshtein_distance, extract_domain_parts


def test_levenshtein_distance():
    assert levenshtein_distance("paypal", "paypal") == 0
    assert levenshtein_distance("paypal", "paypa1") == 1
    assert levenshtein_distance("chase", "chasee") == 1
    assert levenshtein_distance("apple", "orange") > 3
    assert levenshtein_distance("", "test") == 4


def test_extract_domain_parts():
    parts = extract_domain_parts("https://secure.paypa1.com/login?id=123")
    assert parts["host"] == "secure.paypa1.com"
    assert parts["base_domain"] == "paypa1"
    assert parts["tld"] == "com"
    assert parts["is_https"] == 1.0
    assert "secure" in parts["subdomains"]


def test_handcrafted_text_features_urgency_and_links():
    extractor = HandcraftedTextFeatures()
    
    # Scam sample
    scam_text = "URGENT: Your bank account is locked! Act now: http://bit.ly/verify-acct"
    feats_scam = extractor.transform([scam_text])[0]
    names = extractor.get_feature_names_out()
    
    feat_dict = dict(zip(names, feats_scam))
    assert feat_dict["has_url"] == 1.0
    assert feat_dict["url_count"] >= 1.0
    assert feat_dict["urgency_score"] >= 1.0
    assert feat_dict["exclamation_count"] >= 1.0

    # Benign sample
    ham_text = "Hey John, are we having lunch at noon?"
    feats_ham = extractor.transform([ham_text])[0]
    ham_dict = dict(zip(names, feats_ham))
    assert ham_dict["has_url"] == 0.0
    assert ham_dict["urgency_score"] == 0.0


def test_url_feature_extractor_typosquatting_and_ip():
    extractor = URLFeatureExtractor()
    
    # Typosquatting sample
    typo_url = "http://paypa1-security-login.xyz/auth"
    feats_typo = extractor.transform([typo_url])[0]
    names = extractor.get_feature_names_out()
    typo_dict = dict(zip(names, feats_typo))
    
    assert typo_dict["is_suspicious_tld"] == 1.0
    assert typo_dict["is_https"] == 0.0

    # IP host sample
    ip_url = "http://192.168.1.1:8080/login.php"
    feats_ip = extractor.transform([ip_url])[0]
    ip_dict = dict(zip(names, feats_ip))
    assert ip_dict["is_ip_host"] == 1.0
    assert ip_dict["has_port"] == 1.0
