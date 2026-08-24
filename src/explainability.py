"""Explainability Layer: SHAP and Linear Attributions for Multi-Channel Scam Predictions."""

import numpy as np
import pandas as pd
from src.features.text_features import HandcraftedTextFeatures
from src.features.url_features import URLFeatureExtractor, extract_domain_parts


def explain_text_prediction(pipeline, text: str, top_k: int = 5) -> list:
    """Extract top contributing positive and negative factors for text models (SMS / Email)."""
    if not isinstance(text, str) or not text.strip():
        return []

    classifier = pipeline.named_steps["classifier"]
    feature_union = pipeline.named_steps["features"]
    
    tfidf = feature_union.transformer_list[0][1]
    handcrafted = feature_union.transformer_list[1][1]
    
    coefs = classifier.coef_[0]
    
    # 1. TF-IDF features
    tfidf_vec = tfidf.transform([text]).toarray()[0]
    tfidf_names = tfidf.get_feature_names_out()
    
    # 2. Handcrafted features
    hc_vec = handcrafted.transform([text])[0]
    hc_names = handcrafted.get_feature_names_out()
    
    n_tfidf = len(tfidf_names)
    tfidf_coefs = coefs[:n_tfidf]
    hc_coefs = coefs[n_tfidf:]
    
    contributions = []
    
    # Analyze active TF-IDF words
    active_indices = np.where(tfidf_vec > 0)[0]
    for idx in active_indices:
        val = tfidf_vec[idx]
        weight = tfidf_coefs[idx]
        impact = val * weight
        contributions.append({
            "feature": f"Keyword/Phrase: '{tfidf_names[idx]}'",
            "impact": float(impact),
            "value": float(val),
            "type": "nlp_keyword",
            "direction": "Risk Escalator" if impact > 0 else "Safety Indicator"
        })
        
    # Analyze Handcrafted features
    hc_descriptions = {
        "char_length": "Overall message length",
        "word_count": "Total word count",
        "caps_ratio": "Excessive uppercase / screaming letters",
        "digit_ratio": "High numeric character density",
        "exclamation_count": "Multiple exclamation marks",
        "question_count": "Question marks",
        "dollar_count": "Currency / financial symbols ($, £, €)",
        "url_count": "Embedded hyperlinks count",
        "has_url": "Presence of actionable hyperlink",
        "phone_count": "Phone number / SMS shortcode count",
        "has_phone": "Call-to-action phone number present",
        "urgency_score": "Panic / high urgency trigger keywords",
        "inducement_score": "Prize / lottery / reward inducement keywords",
        "brand_mention_count": "High-risk financial/tech brand mentions",
        "has_ip_in_text": "Direct numeric IP address embedded in text"
    }
    
    for i, name in enumerate(hc_names):
        val = hc_vec[i]
        weight = hc_coefs[i] if i < len(hc_coefs) else 0.0
        impact = val * weight
        if val > 0:
            contributions.append({
                "feature": hc_descriptions.get(name, name),
                "impact": float(impact),
                "value": float(val),
                "type": "structural_signal",
                "direction": "Risk Escalator" if impact > 0 else "Safety Indicator"
            })
            
    # Sort by absolute impact
    contributions = sorted(contributions, key=lambda x: abs(x["impact"]), reverse=True)
    return contributions[:top_k]


def explain_url_prediction(pipeline, url: str, top_k: int = 5) -> list:
    """Extract top contributing risk signals and typosquatting insights for URL predictions."""
    if not isinstance(url, str) or not url.strip():
        return []

    classifier = pipeline.named_steps["classifier"]
    extractor = pipeline.named_steps["features"]
    
    features_vec = extractor.transform([url])[0]
    feature_names = extractor.get_feature_names_out()
    
    # Friendly descriptions for URL features
    url_desc = {
        "url_length": "Excessive URL character length",
        "host_length": "Abnormally long host/domain name",
        "path_length": "Deep and obscured path hierarchy",
        "query_length": "Long query parameters",
        "dot_count": "High number of dots in domain/path",
        "hyphen_count": "Multiple hyphens commonly used to impersonate brands",
        "underscore_count": "Underscores in URL string",
        "slash_count": "Multiple path slashes",
        "question_count": "Query parameter markers",
        "at_count": "Use of '@' symbol (often used to obscure destination host)",
        "percent_count": "URL-encoded hex obfuscation (%)",
        "digit_count": "Numeric character count in URL",
        "digit_ratio": "High ratio of digits",
        "subdomain_count": "Deep subdomain nesting structure",
        "is_ip_host": "Direct IP address used instead of legitimate domain",
        "is_https": "HTTPS encryption protocol status",
        "has_port": "Non-standard port specified in URL",
        "is_suspicious_tld": "High-risk / abuse-prone top level domain (.xyz, .top, .ml, etc.)",
        "has_brand_keyword_in_url": "Target brand keyword in path or subdomain",
        "min_levenshtein_to_brand": "Levenshtein edit distance to major brand",
        "max_brand_similarity_ratio": "High similarity ratio to target brand",
        "is_typosquatting_candidate": "Brand typosquatting spoofing detected"
    }

    # Inspect domain parts
    domain_info = extract_domain_parts(url)
    
    contributions = []
    
    # If Tree / Forest / XGBoost model, look at feature importances
    if hasattr(classifier, "feature_importances_"):
        importances = classifier.feature_importances_
        for i, name in enumerate(feature_names):
            val = features_vec[i]
            imp = importances[i]
            # Higher value on risky features triggers positive attribution
            if val > 0:
                contributions.append({
                    "feature": url_desc.get(name, name),
                    "impact": float(imp * (val / (1.0 + abs(val)))),
                    "value": float(val),
                    "direction": "Risk Escalator" if name != "is_https" else ("Safety Indicator" if val == 1.0 else "Risk Escalator")
                })
    else:
        for i, name in enumerate(feature_names):
            val = features_vec[i]
            if val > 0:
                contributions.append({
                    "feature": url_desc.get(name, name),
                    "impact": float(val),
                    "value": float(val),
                    "direction": "Risk Escalator"
                })

    contributions = sorted(contributions, key=lambda x: abs(x["impact"]), reverse=True)
    return contributions[:top_k]
