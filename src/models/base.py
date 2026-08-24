"""Base model utilities, metrics evaluation, and joblib artifact serialization."""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    classification_report
)

ARTIFACTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models_artifacts")
os.makedirs(ARTIFACTS_DIR, exist_ok=True)


def evaluate_model_performance(y_true, y_pred, y_prob=None, model_name: str = "Model") -> dict:
    """Compute comprehensive evaluation metrics with a strong emphasis on Recall and Cost-Sensitivity."""
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel() if cm.shape == (2, 2) else (0, 0, 0, 0)

    metrics = {
        "model_name": model_name,
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
        "total_samples": int(len(y_true))
    }

    if y_prob is not None:
        try:
            metrics["roc_auc"] = float(roc_auc_score(y_true, y_prob))
            metrics["pr_auc"] = float(average_precision_score(y_true, y_prob))
        except Exception:
            metrics["roc_auc"] = None
            metrics["pr_auc"] = None

    print(f"\n==================================================")
    print(f"[METRICS] EVALUATION REPORT: {model_name}")
    print(f"==================================================")
    print(f"Precision: {precision:.4f}  |  Recall: {recall:.4f}  |  F1-Score: {f1:.4f}")
    if "roc_auc" in metrics and metrics["roc_auc"] is not None:
        print(f"ROC-AUC:   {metrics['roc_auc']:.4f}  |  PR-AUC: {metrics['pr_auc']:.4f}")
    print(f"\nConfusion Matrix:")
    print(f"  [TN: {tn:5d} | FP: {fp:5d}] (Actual Ham/Benign)")
    print(f"  [FN: {fn:5d} | TP: {tp:5d}] (Actual Scam/Malicious)")
    print(f"==================================================\n")

    return metrics


def save_pipeline(pipeline, filename: str) -> str:
    """Serialize scikit-learn pipeline to disk using joblib."""
    filepath = os.path.join(ARTIFACTS_DIR, filename)
    joblib.dump(pipeline, filepath)
    print(f"[Artifact Serialization] Saved pipeline to: {filepath}")
    return filepath


def load_pipeline(filename: str):
    """Load serialized scikit-learn pipeline from disk."""
    filepath = os.path.join(ARTIFACTS_DIR, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Model artifact not found at {filepath}. Please train the model first.")
    return joblib.load(filepath)
