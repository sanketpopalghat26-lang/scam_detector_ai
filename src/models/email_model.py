"""Email Phishing Detection Branch: Baseline Logistic Regression + TF-IDF & Handcrafted Features."""

import pandas as pd
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from src.features.text_features import HandcraftedTextFeatures
from src.models.base import evaluate_model_performance, save_pipeline, load_pipeline
from src.ingestion.loaders import load_email_data


def build_email_baseline_pipeline() -> Pipeline:
    """Build Scikit-Learn Pipeline combining TF-IDF and Handcrafted Features with Logistic Regression for Emails."""
    feature_union = FeatureUnion([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=8000,
            sublinear_tf=True,
            lowercase=True,
            strip_accents="unicode"
        )),
        ("handcrafted", HandcraftedTextFeatures())
    ])

    pipeline = Pipeline([
        ("features", feature_union),
        ("classifier", LogisticRegression(
            C=1.5,
            class_weight="balanced",
            max_iter=1000,
            random_state=42,
            solver="liblinear"
        ))
    ])
    return pipeline


def train_email_branch(df: pd.DataFrame = None, test_size: float = 0.2, random_state: int = 42) -> tuple:
    """Train and evaluate the baseline Email phishing model."""
    if df is None:
        df = load_email_data()

    X = df["text"]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    print(f"[Email Branch Training] Training on {len(X_train)} samples, testing on {len(X_test)} samples...")
    pipeline = build_email_baseline_pipeline()
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    metrics = evaluate_model_performance(y_test, y_pred, y_prob, model_name="Email Branch (Baseline LR)")
    save_pipeline(pipeline, "email_baseline.joblib")

    return pipeline, metrics
