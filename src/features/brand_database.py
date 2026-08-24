"""Curated top brand domains and keywords for typosquatting and brand spoofing detection."""

TOP_BRAND_DOMAINS = [
    # Tech & Software
    "google.com", "microsoft.com", "apple.com", "amazon.com", "facebook.com",
    "instagram.com", "whatsapp.com", "netflix.com", "spotify.com", "linkedin.com",
    "twitter.com", "x.com", "tiktok.com", "snapchat.com", "pinterest.com",
    "reddit.com", "github.com", "gitlab.com", "dropbox.com", "adobe.com",
    "salesforce.com", "zoom.us", "slack.com", "openai.com", "yahoo.com",
    "bing.com", "duckduckgo.com", "ebay.com", "paypal.com", "stripe.com",
    "shopify.com", "wordpress.com", "cloudflare.com", "godaddy.com",

    # Banking & Financial Services (Global & US/UK/India)
    "chase.com", "bankofamerica.com", "wellsfargo.com", "citi.com",
    "usbank.com", "capitalone.com", "americanexpress.com", "barclays.co.uk",
    "hsbc.com", "santander.co.uk", "lloydsbank.com", "natwest.com",
    "sbi.co.in", "hdfcbank.com", "icicibank.com", "axisbank.com",
    "anz.com", "commbank.com.au", "westpac.com.au", "nab.com.au",
    "coinbase.com", "binance.com", "kraken.com", "robinhood.com",
    "venmo.com", "cash.app", "zellepay.com", "westernunion.com",

    # Telecom & Delivery Services
    "att.com", "verizon.com", "t-mobile.com", "vodafone.com", "o2.co.uk",
    "usps.com", "fedex.com", "ups.com", "dhl.com", "royalmail.com",
    "dpd.com", "hermesworld.com", "evri.com", "indiapost.gov.in",

    # Government, Tax, Health & Security
    "irs.gov", "gov.uk", "ssa.gov", "hmrc.gov.uk", "cdc.gov", "who.int",
    "docusign.com", "norton.com", "mcafee.com", "bitdefender.com", "kaspersky.com"
]

# High-risk brand names extracted for keyword spoofing analysis
HIGH_RISK_BRAND_KEYWORDS = [
    "paypal", "apple", "google", "microsoft", "amazon", "netflix",
    "chase", "bank of america", "wells fargo", "citibank", "capital one",
    "american express", "hsbc", "barclays", "sbi", "hdfc", "icici",
    "usps", "fedex", "ups", "dhl", "coinbase", "binance", "metamask",
    "irs", "hmrc", "whatsapp", "facebook", "instagram", "docusign",
    "norton", "mcafee", "geek squad", "att", "verizon", "t-mobile"
]

# Suspicious top-level domains commonly abused in phishing/malware campaigns
SUSPICIOUS_TLDS = {
    "xyz", "top", "work", "tk", "ml", "ga", "cf", "gq", "click", "link",
    "zip", "mov", "buzz", "cam", "fit", "rest", "surf", "icu", "monster",
    "country", "stream", "gdn", "party", "trade", "loan", "science", "racing"
}

# Urgency and panic triggers common in smishing/phishing
URGENCY_KEYWORDS = [
    "urgent", "immediately", "act now", "action required", "account suspended",
    "locked", "unauthorized", "suspicious activity", "security alert",
    "verify your account", "confirm your identity", "expire", "compromised",
    "restricted", "disabled", "frozen", "reactivate", "failure to respond",
    "legal action", "arrest warrant", "final notice", "terminated", "breach"
]

# Financial / Reward / Scam inducement triggers
INDUCEMENT_KEYWORDS = [
    "winner", "won", "lottery", "prize", "claim your", "free gift", "reward",
    "cash bonus", "refund", "overdue payment", "bitcoin", "crypto giveaway",
    "investment return", "100% guarantee", "congratulations", "selected for",
    "inheritance", "wire transfer", "western union", "gift card", "claim now"
]
