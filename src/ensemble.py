"""Ensemble and Meta-Model Layer for Multi-Channel Cyber Scam Detection."""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from src.models.base import save_pipeline, load_pipeline


class ScamEnsemble:
    """Multi-channel ensemble aggregator supporting weighted averaging and stacking meta-classification."""

    def __init__(self, weights: dict = None):
        self.weights = weights or {
            "email": 0.35,
            "sms": 0.35,
            "url": 0.30
        }
        self.meta_model = LogisticRegression(C=1.0, random_state=42, solver="liblinear")
        self.is_fitted = False

    def predict_weighted(self, branch_scores: dict) -> tuple:
        """Compute weighted average probability across present branch predictions.
        
        Args:
            branch_scores: dict containing available channel probabilities, e.g. {'email': 0.85, 'url': 0.92}
        Returns:
            (verdict, score, details)
        """
        valid_scores = {k: v for k, v in branch_scores.items() if v is not None and k in self.weights}
        if not valid_scores:
            return "BENIGN", 0.0, {}

        # Re-normalize weights for available modalities
        total_weight = sum(self.weights[k] for k in valid_scores.keys())
        normalized_weights = {k: self.weights[k] / total_weight for k in valid_scores.keys()}

        ensemble_prob = sum(valid_scores[k] * normalized_weights[k] for k in valid_scores.keys())
        verdict = "SCAM" if ensemble_prob >= 0.50 else "BENIGN"

        return verdict, float(ensemble_prob), {
            "method": "weighted_average",
            "channel_scores": valid_scores,
            "applied_weights": normalized_weights
        }

    def fit_meta_model(self, X_meta: np.ndarray, y_meta: np.ndarray):
        """Train Stacking Meta-Classifier (Logistic Regression) on out-of-fold branch probabilities."""
        self.meta_model.fit(X_meta, y_meta)
        self.is_fitted = True
        print("[Ensemble] Stacking meta-model successfully trained.")
        return self

    def predict_meta(self, branch_scores_matrix: np.ndarray) -> tuple:
        """Predict using fitted stacking meta-classifier."""
        if not self.is_fitted:
            raise RuntimeError("Stacking meta-model is not fitted yet.")

        probs = self.meta_model.predict_proba(branch_scores_matrix)[:, 1]
        preds = (probs >= 0.5).astype(int)
        return preds, probs


def build_and_save_ensemble() -> ScamEnsemble:
    """Instantiate, fit with benchmark meta-data, and serialize ensemble artifact."""
    ensemble = ScamEnsemble()
    
    # Synthetic out-of-fold calibration matrix for meta-model
    np.random.seed(42)
    n_samples = 600
    y = np.random.binomial(1, 0.5, n_samples)
    
    # Correlate branch predictions with ground truth
    sms_prob = np.clip(y * 0.85 + np.random.normal(0.08, 0.12, n_samples), 0.01, 0.99)
    email_prob = np.clip(y * 0.88 + np.random.normal(0.06, 0.11, n_samples), 0.01, 0.99)
    url_prob = np.clip(y * 0.82 + np.random.normal(0.09, 0.13, n_samples), 0.01, 0.99)
    
    X_meta = np.column_stack([sms_prob, email_prob, url_prob])
    ensemble.fit_meta_model(X_meta, y)
    
    save_pipeline(ensemble, "ensemble_model.joblib")
    return ensemble
