"""CLI Training Orchestrator for Multi-Channel Cyber Scam Detector.
Trains SMS, Email, URL branches, and the Ensemble meta-model.
"""

import argparse
import json
import os
import sys

# Ensure UTF-8 output encoding on Windows consoles
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
from src.models.sms_model import train_sms_branch
from src.models.email_model import train_email_branch
from src.models.url_model import train_url_branch
from src.ensemble import build_and_save_ensemble


def run_training_pipeline(branch: str = "all", test_size: float = 0.2, random_state: int = 42) -> dict:
    """Execute end-to-end training and metric evaluation."""
    results = {}
    print(f"\n=======================================================")
    print(f"[START] INITIATING MULTI-CHANNEL SCAM DETECTOR TRAINING ({branch.upper()})")
    print(f"=======================================================\n")

    # 1. SMS Branch
    if branch in ["sms", "all"]:
        print("\n--- [Step 1/4] Training SMS Branch (Smishing Baseline) ---")
        sms_pipeline, sms_metrics = train_sms_branch(test_size=test_size, random_state=random_state)
        results["sms_baseline"] = sms_metrics

    # 2. Email Branch
    if branch in ["email", "all"]:
        print("\n--- [Step 2/4] Training Email Branch (Phishing Baseline) ---")
        email_pipeline, email_metrics = train_email_branch(test_size=test_size, random_state=random_state)
        results["email_baseline"] = email_metrics

    # 3. URL Branch (Domain-Grouped Split)
    if branch in ["url", "all"]:
        print("\n--- [Step 3/4] Training URL Branch (Malicious Link XGBoost) ---")
        url_pipeline, url_metrics = train_url_branch(test_size=test_size, random_state=random_state, model_type="xgboost")
        results["url_model"] = url_metrics

    # 4. Ensemble Meta-Model
    if branch in ["ensemble", "all"]:
        print("\n--- [Step 4/4] Building & Calibrating Ensemble Layer ---")
        ensemble = build_and_save_ensemble()
        results["ensemble"] = {
            "status": "trained_and_serialized",
            "weights": ensemble.weights
        }

    # Save summary report
    metrics_file = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "models_artifacts",
        "training_metrics.json"
    )
    with open(metrics_file, "w") as f:
        json.dump(results, f, indent=2)

    print("\n=======================================================")
    print("[SUCCESS] TRAINING PIPELINE COMPLETE! All artifacts saved.")
    print(f"Metrics saved to: {metrics_file}")
    print("=======================================================\n")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Multi-Channel Scam Detector Branches")
    parser.add_argument(
        "--branch",
        type=str,
        default="all",
        choices=["all", "sms", "email", "url", "ensemble"],
        help="Target branch to train (default: all)"
    )
    parser.add_argument("--test_size", type=float, default=0.2, help="Test split proportion")
    parser.add_argument("--random_state", type=int, default=42, help="Random seed")

    args = parser.parse_args()
    run_training_pipeline(branch=args.branch, test_size=args.test_size, random_state=args.random_state)
