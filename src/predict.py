"""Unified multi-channel prediction engine with explainability.
Supports CLI arguments and programmatic invocations.
"""

import argparse
import json
import os
import sys
import re

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.models.base import load_pipeline
from src.explainability import explain_text_prediction, explain_url_prediction
from src.features.text_features import URL_REGEX


class ScamPredictor:
    """Unified inference engine for SMS, Email, URL, and compound multi-channel incidents."""

    def __init__(self):
        self.sms_model = None
        self.email_model = None
        self.url_model = None
        self.ensemble = None
        self._load_models()

    def _load_models(self):
        """Lazy load or initialize model pipelines."""
        try:
            self.sms_model = load_pipeline("sms_baseline.joblib")
        except Exception as e:
            print(f"[Warning] Could not load SMS model: {e}")

        try:
            self.email_model = load_pipeline("email_baseline.joblib")
        except Exception as e:
            print(f"[Warning] Could not load Email model: {e}")

        try:
            self.url_model = load_pipeline("url_model.joblib")
        except Exception as e:
            print(f"[Warning] Could not load URL model: {e}")

        try:
            self.ensemble = load_pipeline("ensemble_model.joblib")
        except Exception as e:
            print(f"[Warning] Could not load Ensemble model: {e}")

    def predict_sms(self, text: str) -> dict:
        """Analyze SMS for Smishing threat."""
        if not self.sms_model:
            self._load_models()
        if not self.sms_model:
            raise RuntimeError("SMS model not trained yet. Run `python src/train.py --branch sms` first.")

        prob = float(self.sms_model.predict_proba([text])[0][1])
        verdict = "SCAM" if prob >= 0.50 else "BENIGN"
        risk_level = self._get_risk_level(prob)
        explanations = explain_text_prediction(self.sms_model, text, top_k=5)

        # Check if SMS has embedded URL to scan
        embedded_urls = URL_REGEX.findall(text)
        url_results = []
        if embedded_urls and self.url_model:
            for u in embedded_urls:
                url_res = self.predict_url(u)
                url_results.append(url_res)

        return {
            "channel": "sms",
            "verdict": verdict,
            "confidence": round(prob, 4),
            "risk_score_pct": round(prob * 100, 1),
            "risk_level": risk_level,
            "input_preview": text[:120] + ("..." if len(text) > 120 else ""),
            "top_factors": explanations,
            "embedded_urls_analysis": url_results
        }

    def predict_email(self, text: str) -> dict:
        """Analyze Email for Phishing threat."""
        if not self.email_model:
            self._load_models()
        if not self.email_model:
            raise RuntimeError("Email model not trained yet. Run `python src/train.py --branch email` first.")

        prob = float(self.email_model.predict_proba([text])[0][1])
        verdict = "SCAM" if prob >= 0.50 else "BENIGN"
        risk_level = self._get_risk_level(prob)
        explanations = explain_text_prediction(self.email_model, text, top_k=6)

        # Check if email contains embedded URLs
        embedded_urls = URL_REGEX.findall(text)
        url_results = []
        if embedded_urls and self.url_model:
            for u in embedded_urls:
                url_res = self.predict_url(u)
                url_results.append(url_res)

        return {
            "channel": "email",
            "verdict": verdict,
            "confidence": round(prob, 4),
            "risk_score_pct": round(prob * 100, 1),
            "risk_level": risk_level,
            "input_preview": text[:120] + ("..." if len(text) > 120 else ""),
            "top_factors": explanations,
            "embedded_urls_analysis": url_results
        }

    def predict_url(self, url: str) -> dict:
        """Analyze URL for Malicious / Phishing threat."""
        if not self.url_model:
            self._load_models()
        if not self.url_model:
            raise RuntimeError("URL model not trained yet. Run `python src/train.py --branch url` first.")

        prob = float(self.url_model.predict_proba([url])[0][1])
        verdict = "SCAM" if prob >= 0.50 else "BENIGN"
        risk_level = self._get_risk_level(prob)
        explanations = explain_url_prediction(self.url_model, url, top_k=6)

        return {
            "channel": "url",
            "verdict": verdict,
            "confidence": round(prob, 4),
            "risk_score_pct": round(prob * 100, 1),
            "risk_level": risk_level,
            "url": url,
            "top_factors": explanations
        }

    def predict_incident(self, email_text: str = None, sms_text: str = None, url: str = None) -> dict:
        """Multi-channel compound incident risk assessment."""
        branch_scores = {}
        branch_details = {}

        if email_text:
            res = self.predict_email(email_text)
            branch_scores["email"] = res["confidence"]
            branch_details["email"] = res

        if sms_text:
            res = self.predict_sms(sms_text)
            branch_scores["sms"] = res["confidence"]
            branch_details["sms"] = res

        if url:
            res = self.predict_url(url)
            branch_scores["url"] = res["confidence"]
            branch_details["url"] = res

        if not self.ensemble:
            self._load_models()

        if self.ensemble and branch_scores:
            verdict, ensemble_score, meta_info = self.ensemble.predict_weighted(branch_scores)
        else:
            scores = list(branch_scores.values())
            ensemble_score = float(np.mean(scores)) if scores else 0.0
            verdict = "SCAM" if ensemble_score >= 0.50 else "BENIGN"
            meta_info = {"method": "simple_average"}

        return {
            "overall_verdict": verdict,
            "overall_confidence": round(ensemble_score, 4),
            "overall_risk_score_pct": round(ensemble_score * 100, 1),
            "overall_risk_level": self._get_risk_level(ensemble_score),
            "ensemble_metadata": meta_info,
            "branches": branch_details
        }

    @staticmethod
    def _get_risk_level(score: float) -> str:
        if score >= 0.85:
            return "CRITICAL"
        elif score >= 0.65:
            return "HIGH"
        elif score >= 0.40:
            return "MEDIUM"
        elif score >= 0.20:
            return "LOW"
        else:
            return "SAFE"


# Ensure UTF-8 output encoding on Windows consoles
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Channel Cyber Scam Predictor")
    parser.add_argument("--channel", type=str, choices=["sms", "email", "url", "incident"], required=True)
    parser.add_argument("--text", type=str, help="SMS or Email content to evaluate")
    parser.add_argument("--url", type=str, help="URL link to evaluate")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()
    predictor = ScamPredictor()

    if args.channel == "sms":
        if not args.text:
            print("Error: --text is required for SMS channel.")
            exit(1)
        res = predictor.predict_sms(args.text)
    elif args.channel == "email":
        if not args.text:
            print("Error: --text is required for Email channel.")
            exit(1)
        res = predictor.predict_email(args.text)
    elif args.channel == "url":
        if not args.url:
            print("Error: --url is required for URL channel.")
            exit(1)
        res = predictor.predict_url(args.url)
    elif args.channel == "incident":
        res = predictor.predict_incident(email_text=args.text, url=args.url)

    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"\n=======================================================")
        print(f"[VERDICT] SCAM DETECTION RESULT: {res.get('verdict', res.get('overall_verdict'))}")
        print(f"Risk Level:  {res.get('risk_level', res.get('overall_risk_level'))}")
        print(f"Confidence:  {res.get('confidence', res.get('overall_confidence')) * 100:.1f}%")
        print(f"=======================================================")
        factors = res.get("top_factors", [])
        if factors:
            print("Key Contributing Factors:")
            for f in factors:
                print(f"  * {f['direction']}: {f['feature']} (Score delta: {f['impact']:+.3f})")
        print("=======================================================\n")
