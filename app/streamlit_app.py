"""Streamlit Web Application: Multi-Channel Cyber Scam Detection Dashboard.
Provides real-time interactive threat classification, explainability, and multi-channel incident aggregation.
"""

import sys
import os

# Ensure project root is in sys.path when running from app/ directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd
import numpy as np
import json
import time

# Set page configuration
st.set_page_config(
    page_title="AI Cyber Scam Detector | Multi-Channel Defense",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for rich dark cyber aesthetics
st.markdown("""
<style>
    /* Global Styling */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    
    /* Headers & Typography */
    h1, h2, h3 {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 700;
    }
    .main-title {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    
    /* Metric Cards */
    .cyber-card {
        background: rgba(17, 24, 39, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.25rem;
        backdrop-filter: blur(10px);
        margin-bottom: 1rem;
    }
    
    .verdict-badge-scam {
        background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 700;
        letter-spacing: 1px;
        display: inline-block;
        box-shadow: 0 4px 14px rgba(239, 68, 68, 0.35);
    }
    
    .verdict-badge-benign {
        background: linear-gradient(135deg, #10b981 0%, #047857 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 700;
        letter-spacing: 1px;
        display: inline-block;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35);
    }
    
    .factor-item {
        padding: 8px 12px;
        margin: 6px 0;
        border-radius: 6px;
        background: rgba(255, 255, 255, 0.03);
        border-left: 3px solid #6366f1;
        font-size: 0.92rem;
    }
    .factor-risk {
        border-left-color: #ef4444;
    }
    .factor-safe {
        border-left-color: #10b981;
    }
</style>
""", unsafe_allow_html=True)

# Try importing model predictor
try:
    from src.predict import ScamPredictor
    from src.features.url_features import extract_domain_parts
    predictor = ScamPredictor()
except Exception as e:
    predictor = None
    st.error(f"Error initializing predictor: {e}. Please ensure models are trained.")

# Header
st.markdown('<div class="main-title">🛡️ Multi-Channel Cyber Scam & Fraud Detector</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Production-grade multi-vector threat classification for Phishing Emails, Smishing SMS, and Malicious URLs with explainable AI.</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/isometric/512/cyber-security.png", width=70)
    st.title("System Controls")
    st.markdown("---")
    st.markdown("### 🔍 Model Architecture")
    st.markdown("""
    - **SMS Branch**: TF-IDF + Handcrafted Signals (LR)
    - **Email Branch**: TF-IDF + Brand Spoofing (LR)
    - **URL Branch**: XGBoost on Lexical + Levenshtein Distance
    - **Ensemble Layer**: Stacking Meta-Classifier
    """)
    st.markdown("---")
    st.markdown("### ⚖️ Anti-Leakage Rigor")
    st.info("URL model uses **Domain-Grouped Split** (`GroupShuffleSplit`) to prevent inflated evaluation metrics.")
    st.markdown("---")
    st.caption("Designed for Security & Fraud Prevention Teams")

# Main Navigation Tabs
tab_sms, tab_email, tab_url, tab_incident, tab_metrics = st.tabs([
    "📱 SMS Smishing",
    "📧 Email Phishing",
    "🔗 Malicious URL",
    "🛡️ Compound Incident",
    "📊 Metrics & Explainability"
])


# ====================================================================
# TAB 1: SMS Smishing
# ====================================================================
with tab_sms:
    st.subheader("📱 SMS Smishing Detection")
    st.markdown("Analyze incoming SMS text messages for fraud, account takeovers, and fraudulent payment lures.")

    col1, col2 = st.columns([1.2, 0.8])

    with col1:
        # Predefined demo buttons
        st.markdown("**Quick Test Samples:**")
        bcol1, bcol2 = st.columns(2)
        sms_default = ""
        if bcol1.button("🚨 Urgent Bank Scam SMS", key="demo_sms_scam"):
            sms_default = "URGENT: Your Chase bank account has been suspended due to suspicious activity. Verify now at http://secure-chase-update.xyz"
        if bcol2.button("✅ Legitimate SMS", key="demo_sms_ham"):
            sms_default = "Hey Sarah, are we still meeting for lunch at 12:30 today?"

        sms_input = st.text_area("Paste SMS Message Content:", value=sms_default, height=140, placeholder="e.g. URGENT: Action required on your account...")
        analyze_sms = st.button("🚀 Analyze SMS", type="primary", use_container_width=True)

    with col2:
        if (analyze_sms or sms_input) and sms_input.strip() and predictor:
            with st.spinner("Evaluating SMS features..."):
                res = predictor.predict_sms(sms_input)

            is_scam = res["verdict"] == "SCAM"
            badge_class = "verdict-badge-scam" if is_scam else "verdict-badge-benign"
            badge_icon = "🚨" if is_scam else "✅"

            st.markdown(f'<div class="{badge_class}">{badge_icon} VERDICT: {res["verdict"]}</div>', unsafe_allow_html=True)
            st.markdown(f"### Scam Risk Score: **{res['risk_score_pct']}%** ({res['risk_level']})")
            st.progress(res["confidence"])

            st.markdown("#### 🔍 Top Explanatory Factors:")
            for f in res.get("top_factors", []):
                card_class = "factor-risk" if f["direction"] == "Risk Escalator" else "factor-safe"
                st.markdown(f'<div class="factor-item {card_class}"><b>{f["direction"]}:</b> {f["feature"]} (Weight: {f["impact"]:+.3f})</div>', unsafe_allow_html=True)

            if res.get("embedded_urls_analysis"):
                st.markdown("#### 🔗 Embedded URL Threat Assessment:")
                for u_res in res["embedded_urls_analysis"]:
                    u_scam = u_res["verdict"] == "SCAM"
                    u_badge = "🚨 Threat" if u_scam else "✅ Benign"
                    st.write(f"- `{u_res['url']}`: **{u_badge}** (Risk: {u_res['risk_score_pct']}%)")


# ====================================================================
# TAB 2: Email Phishing
# ====================================================================
with tab_email:
    st.subheader("📧 Email Phishing & Spear-Phishing Detection")
    st.markdown("Evaluate email bodies and headers for brand spoofing, urgent credential harvesting, and fraudulent lures.")

    col1, col2 = st.columns([1.2, 0.8])

    with col1:
        st.markdown("**Quick Test Samples:**")
        ecol1, ecol2 = st.columns(2)
        email_default = ""
        if ecol1.button("🚨 Phishing Email Sample", key="demo_email_scam"):
            email_default = "Subject: URGENT: Action Required on Your PayPal Account\n\nDear Customer,\nWe detected unauthorized login attempts from an unknown IP address. To avoid account suspension, click here to verify your identity: http://paypa1-security-login.xyz/auth\n\nSecurity Team"
        if ecol2.button("✅ Safe Work Email Sample", key="demo_email_ham"):
            email_default = "Subject: Sprint Review Notes and Next Steps\n\nHi Team,\nHere are the notes from our sprint review. Great job hitting our milestones. Let's sync tomorrow at 10 AM.\n\nBest,\nAlex"

        email_input = st.text_area("Paste Email Text (Subject & Body):", value=email_default, height=180, placeholder="Subject: ...\n\nEmail body...")
        analyze_email = st.button("🚀 Analyze Email", type="primary", use_container_width=True)

    with col2:
        if (analyze_email or email_input) and email_input.strip() and predictor:
            with st.spinner("Analyzing email semantics and header markers..."):
                res = predictor.predict_email(email_input)

            is_scam = res["verdict"] == "SCAM"
            badge_class = "verdict-badge-scam" if is_scam else "verdict-badge-benign"
            badge_icon = "🚨" if is_scam else "✅"

            st.markdown(f'<div class="{badge_class}">{badge_icon} VERDICT: {res["verdict"]}</div>', unsafe_allow_html=True)
            st.markdown(f"### Phishing Risk Score: **{res['risk_score_pct']}%** ({res['risk_level']})")
            st.progress(res["confidence"])

            st.markdown("#### 🔍 Top Explanatory Factors:")
            for f in res.get("top_factors", []):
                card_class = "factor-risk" if f["direction"] == "Risk Escalator" else "factor-safe"
                st.markdown(f'<div class="factor-item {card_class}"><b>{f["direction"]}:</b> {f["feature"]} (Weight: {f["impact"]:+.3f})</div>', unsafe_allow_html=True)

            if res.get("embedded_urls_analysis"):
                st.markdown("#### 🔗 Extracted URL Threat Breakdown:")
                for u_res in res["embedded_urls_analysis"]:
                    u_scam = u_res["verdict"] == "SCAM"
                    u_badge = "🚨 Suspicious" if u_scam else "✅ Safe"
                    st.write(f"- `{u_res['url']}`: **{u_badge}** ({u_res['risk_score_pct']}%)")


# ====================================================================
# TAB 3: Malicious URL Scanner
# ====================================================================
with tab_url:
    st.subheader("🔗 Malicious URL & Brand Typosquatting Scanner")
    st.markdown("Detect weaponized domains, typosquatting (`paypa1.com`), suspicious TLDs, IP-based hosts, and deceptive paths.")

    col1, col2 = st.columns([1.2, 0.8])

    with col1:
        st.markdown("**Quick Test Samples:**")
        ucol1, ucol2, ucol3 = st.columns(3)
        url_default = ""
        if ucol1.button("🚨 Typosquat URL", key="demo_url_typo"):
            url_default = "http://paypa1-security-login.xyz/auth/verify"
        if ucol2.button("🚨 IP Host URL", key="demo_url_ip"):
            url_default = "http://192.168.1.105:8080/admin/login.php"
        if ucol3.button("✅ Legitimate URL", key="demo_url_legit"):
            url_default = "https://www.paypal.com/signin"

        url_input = st.text_input("Enter Target URL:", value=url_default, placeholder="https://example.com/login")
        analyze_url = st.button("🚀 Analyze URL", type="primary", use_container_width=True)

        if url_input.strip():
            domain_info = extract_domain_parts(url_input)
            st.markdown("#### 🌐 Domain Decomposition")
            st.json({
                "Host": domain_info["host"],
                "Base Domain": domain_info["base_domain"],
                "TLD": domain_info["tld"],
                "Subdomains": domain_info["subdomains"],
                "HTTPS Encryption": "Yes" if domain_info["is_https"] else "No",
                "Non-Standard Port": "Yes" if domain_info["has_port"] else "No"
            })

    with col2:
        if (analyze_url or url_input) and url_input.strip() and predictor:
            with st.spinner("Extracting structural features and checking brand distances..."):
                res = predictor.predict_url(url_input)

            is_scam = res["verdict"] == "SCAM"
            badge_class = "verdict-badge-scam" if is_scam else "verdict-badge-benign"
            badge_icon = "🚨" if is_scam else "✅"

            st.markdown(f'<div class="{badge_class}">{badge_icon} VERDICT: {res["verdict"]}</div>', unsafe_allow_html=True)
            st.markdown(f"### Malicious Risk Score: **{res['risk_score_pct']}%** ({res['risk_level']})")
            st.progress(res["confidence"])

            st.markdown("#### 🔍 Top Contributing Risk Signals:")
            for f in res.get("top_factors", []):
                card_class = "factor-risk" if f["direction"] == "Risk Escalator" else "factor-safe"
                st.markdown(f'<div class="factor-item {card_class}"><b>{f["direction"]}:</b> {f["feature"]} (Impact: {f["impact"]:+.3f})</div>', unsafe_allow_html=True)


# ====================================================================
# TAB 4: Compound Incident Multi-Channel Analyzer
# ====================================================================
with tab_incident:
    st.subheader("🛡️ Multi-Channel Incident Aggregation")
    st.markdown("Combine signals across text content and embedded URLs through the Stacking Meta-Classifier.")

    inc_email = st.text_area("Incident Email/SMS Body:", height=100, placeholder="Paste incident message body...")
    inc_url = st.text_input("Associated Target URL (optional):", placeholder="https://...")
    analyze_inc = st.button("⚡ Run Multi-Channel Ensemble Assessment", type="primary")

    if analyze_inc and (inc_email or inc_url) and predictor:
        with st.spinner("Aggregating multi-channel signals through Stacking Meta-Model..."):
            inc_res = predictor.predict_incident(email_text=inc_email, url=inc_url)

        is_scam = inc_res["overall_verdict"] == "SCAM"
        badge_class = "verdict-badge-scam" if is_scam else "verdict-badge-benign"
        badge_icon = "🚨" if is_scam else "✅"

        st.markdown(f'<div class="{badge_class}">{badge_icon} UNIFIED INCIDENT VERDICT: {inc_res["overall_verdict"]}</div>', unsafe_allow_html=True)
        st.markdown(f"### Ensemble Calibrated Risk: **{inc_res['overall_risk_score_pct']}%** ({inc_res['overall_risk_level']})")
        st.progress(inc_res["overall_confidence"])

        st.markdown("#### 📊 Branch Contribution Breakdown:")
        b_cols = st.columns(len(inc_res["branches"])) if inc_res["branches"] else [st.container()]
        for idx, (b_name, b_data) in enumerate(inc_res["branches"].items()):
            with b_cols[idx]:
                st.metric(label=f"Branch: {b_name.upper()}", value=f"{b_data['risk_score_pct']}%", delta=b_data["verdict"])


# ====================================================================
# TAB 5: Metrics & Architecture
# ====================================================================
with tab_metrics:
    st.subheader("📊 Production Metrics & Architectural Validation")
    
    # Try reading saved metrics
    metrics_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models_artifacts", "training_metrics.json")
    if os.path.exists(metrics_path):
        with open(metrics_path, "r") as f:
            metrics_data = json.load(f)
            
        st.markdown("### 🏆 Branch Performance Summary")
        rows = []
        for branch_key, data in metrics_data.items():
            if isinstance(data, dict) and "precision" in data:
                rows.append({
                    "Branch / Model": data.get("model_name", branch_key),
                    "Precision": f"{data.get('precision', 0):.4f}",
                    "Recall": f"{data.get('recall', 0):.4f}",
                    "F1-Score": f"{data.get('f1', 0):.4f}",
                    "ROC-AUC": f"{data.get('roc_auc', 0):.4f}" if data.get('roc_auc') else "N/A",
                    "False Negatives": data.get("false_negatives", 0),
                    "Total Test Samples": data.get("total_samples", 0)
                })
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True)
    else:
        st.info("Metrics will populate after running model training (`python src/train.py`).")

    st.markdown("---")
    st.markdown("### [COST] Cost-Sensitive Optimization Rationale")
    st.markdown(r"""
    In cyber fraud detection, **False Negatives (missed phishing/smishing/malicious URLs) carry catastrophic consequences** (credential theft, wire fraud, ransomware deployment), whereas **False Positives only cause minor friction** (extra user confirmation or secondary sandbox checks).
    
    Therefore, our classification pipelines and thresholds are deliberately calibrated to **maximize Recall ($\ge 98\%$)** while maintaining strong precision.
    """)

    st.markdown("---")
    st.markdown("### [DATA] Zero-Leakage URL Domain-Grouped Splitting")
    st.markdown(r"""
    Standard random train/test splits on URL datasets suffer from severe **data leakage**: multiple URLs sharing the exact same registered domain (`eTLD+1`) appear in both train and test sets, artificially inflating benchmark metrics.
    
    We employ **`GroupShuffleSplit` on domain groups**, ensuring the test set contains strictly unseen base domains.
    """)
