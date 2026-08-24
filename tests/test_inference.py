"""Integration tests for multi-channel scam detector inference engine."""

import pytest
from src.models.sms_model import build_sms_baseline_pipeline
from src.models.email_model import build_email_baseline_pipeline
from src.models.url_model import build_url_rf_pipeline
from src.ensemble import ScamEnsemble


def test_sms_pipeline_fit_and_predict():
    pipeline = build_sms_baseline_pipeline()
    X = [
        "URGENT: Verify your bank account now http://scam.xyz",
        "Hello mate, see you tomorrow at the office"
    ]
    y = [1, 0]
    pipeline.fit(X, y)
    
    preds = pipeline.predict(X)
    probs = pipeline.predict_proba(X)
    
    assert len(preds) == 2
    assert probs.shape == (2, 2)


def test_url_pipeline_fit_and_predict():
    pipeline = build_url_rf_pipeline()
    X = [
        "http://paypa1-security.xyz/login",
        "https://www.paypal.com/home"
    ]
    y = [1, 0]
    pipeline.fit(X, y)
    
    preds = pipeline.predict(X)
    assert len(preds) == 2


def test_ensemble_weighted_prediction():
    ensemble = ScamEnsemble()
    
    # Scam scenario across modalities
    verdict, score, details = ensemble.predict_weighted({"sms": 0.95, "url": 0.90})
    assert verdict == "SCAM"
    assert score > 0.85
    
    # Safe scenario
    verdict_safe, score_safe, _ = ensemble.predict_weighted({"email": 0.05, "url": 0.10})
    assert verdict_safe == "BENIGN"
    assert score_safe < 0.20
