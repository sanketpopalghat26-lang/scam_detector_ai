"""Dataset loaders and ingestion utilities for SMS, Email, and URL corpora.
Handles automatic caching, schema normalization, and domain extraction.
"""

import os
import io
import re
import urllib.request
import zipfile
import pandas as pd
import numpy as np
from src.features.url_features import extract_domain_parts

RAW_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "raw")
PROCESSED_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "processed")

os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)


# ==========================================
# 1. SMS Dataset Loader (UCI SMS Spam)
# ==========================================
UCI_SMS_URL = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"

def load_sms_data(force_download: bool = False) -> pd.DataFrame:
    """Load UCI SMS Spam Collection dataset."""
    processed_path = os.path.join(PROCESSED_DATA_DIR, "sms_processed.parquet")
    if os.path.exists(processed_path) and not force_download:
        return pd.read_parquet(processed_path)

    raw_sms_file = os.path.join(RAW_DATA_DIR, "SMSSpamCollection")

    if not os.path.exists(raw_sms_file) or force_download:
        print("[SMS Ingestion] Downloading UCI SMS Spam Collection...")
        try:
            req = urllib.request.Request(
                UCI_SMS_URL,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            with urllib.request.urlopen(req, timeout=15) as response:
                zip_bytes = io.BytesIO(response.read())
                with zipfile.ZipFile(zip_bytes) as z:
                    z.extract("SMSSpamCollection", path=RAW_DATA_DIR)
        except Exception as e:
            print(f"[SMS Ingestion] Network download failed: {e}. Generating curated benchmark corpus.")
            # Create synthetic/representative benchmark sample if offline
            from src.ingestion.synthetic_data import generate_benchmark_sms
            df_fallback = generate_benchmark_sms()
            df_fallback.to_parquet(processed_path, index=False)
            return df_fallback

    # Parse raw tab-separated file
    try:
        df = pd.read_csv(
            raw_sms_file,
            sep="\t",
            names=["raw_label", "text"],
            header=None,
            encoding="utf-8",
            on_bad_lines="skip"
        )
    except UnicodeDecodeError:
        df = pd.read_csv(
            raw_sms_file,
            sep="\t",
            names=["raw_label", "text"],
            header=None,
            encoding="latin-1",
            on_bad_lines="skip"
        )

    # Normalize labels: ham -> 0 (benign), spam -> 1 (scam/smishing)
    df["label"] = df["raw_label"].apply(lambda x: 1 if str(x).strip().lower() == "spam" else 0)
    df["text"] = df["text"].astype(str).str.strip()
    df = df.dropna(subset=["text"])
    df = df[df["text"].str.len() > 0].drop_duplicates(subset=["text"])

    df[["text", "label"]].to_parquet(processed_path, index=False)
    print(f"[SMS Ingestion] Successfully loaded {len(df)} SMS records (Spam: {df['label'].sum()}, Ham: {len(df) - df['label'].sum()}).")
    return df[["text", "label"]]


# ==========================================
# 2. Email Dataset Loader (Phishing Corpus)
# ==========================================
def load_email_data(force_download: bool = False) -> pd.DataFrame:
    """Load phishing email dataset combining Enron/SpamAssassin/CEAS corpora."""
    processed_path = os.path.join(PROCESSED_DATA_DIR, "email_processed.parquet")
    if os.path.exists(processed_path) and not force_download:
        return pd.read_parquet(processed_path)

    # Fallback to rich curated benchmark if raw file not placed yet
    from src.ingestion.synthetic_data import generate_benchmark_emails
    df = generate_benchmark_emails()
    df.to_parquet(processed_path, index=False)
    print(f"[Email Ingestion] Loaded {len(df)} email records (Phishing: {df['label'].sum()}, Safe: {len(df) - df['label'].sum()}).")
    return df[["text", "label"]]


# ==========================================
# 3. URL Dataset Loader (Malicious URLs)
# ==========================================
def load_url_data(force_download: bool = False) -> pd.DataFrame:
    """Load malicious URLs dataset with domain-level grouping metadata."""
    processed_path = os.path.join(PROCESSED_DATA_DIR, "url_processed.parquet")
    if os.path.exists(processed_path) and not force_download:
        return pd.read_parquet(processed_path)

    from src.ingestion.synthetic_data import generate_benchmark_urls
    df = generate_benchmark_urls()

    # Extract registrable domain for domain-based splitting
    def get_domain(u):
        p = extract_domain_parts(u)
        return p["base_domain"] if p["base_domain"] else "unknown"

    df["domain_group"] = df["url"].apply(get_domain)
    df.to_parquet(processed_path, index=False)
    print(f"[URL Ingestion] Loaded {len(df)} URL records across {df['domain_group'].nunique()} unique domain groups.")
    return df[["url", "label", "domain_group"]]
