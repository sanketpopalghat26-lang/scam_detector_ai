"""URL Malicious Link Detection Branch: Random Forest & XGBoost with Domain-Based Splitting."""

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupShuffleSplit
try:
    import xgboost as xgb
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False

from src.features.url_features import URLFeatureExtractor
from src.models.base import evaluate_model_performance, save_pipeline, load_pipeline
from src.ingestion.loaders import load_url_data


def build_url_rf_pipeline() -> Pipeline:
    """Build URL classification pipeline using Random Forest."""
    return Pipeline([
        ("features", URLFeatureExtractor()),
        ("scaler", StandardScaler()),
        ("classifier", RandomForestClassifier(
            n_estimators=150,
            max_depth=12,
            min_samples_split=4,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1
        ))
    ])


def build_url_xgb_pipeline() -> Pipeline:
    """Build URL classification pipeline using XGBoost (or Random Forest fallback)."""
    if not HAS_XGBOOST:
        return build_url_rf_pipeline()

    return Pipeline([
        ("features", URLFeatureExtractor()),
        ("scaler", StandardScaler()),
        ("classifier", xgb.XGBClassifier(
            n_estimators=150,
            max_depth=6,
            learning_rate=0.08,
            subsample=0.85,
            colsample_bytree=0.85,
            scale_pos_weight=1.2,
            random_state=42,
            eval_metric="logloss"
        ))
    ])


def train_url_branch(
    df: pd.DataFrame = None,
    test_size: float = 0.2,
    random_state: int = 42,
    model_type: str = "xgboost"
) -> tuple:
    """Train URL branch using Domain-Based Splitting to prevent data leakage."""
    if df is None:
        df = load_url_data()

    X = df["url"]
    y = df["label"]
    groups = df["domain_group"]

    # Strict Domain-Based Splitting
    gss = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=random_state)
    train_idx, test_idx = next(gss.split(X, y, groups=groups))

    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
    train_domains = set(groups.iloc[train_idx])
    test_domains = set(groups.iloc[test_idx])
    overlap = train_domains.intersection(test_domains)

    print(f"[URL Domain-Based Split] Train samples: {len(X_train)} ({len(train_domains)} domains)")
    print(f"[URL Domain-Based Split] Test samples:  {len(X_test)} ({len(test_domains)} domains)")
    print(f"[URL Domain-Based Split] Domain overlap count: {len(overlap)} (Zero leakage verified!)")

    # Select pipeline
    if model_type.lower() == "xgboost":
        pipeline = build_url_xgb_pipeline()
        name = "URL Branch (XGBoost - Domain Split)"
    else:
        pipeline = build_url_rf_pipeline()
        name = "URL Branch (Random Forest - Domain Split)"

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    metrics = evaluate_model_performance(y_test, y_pred, y_prob, model_name=name)
    save_pipeline(pipeline, "url_model.joblib")

    return pipeline, metrics
