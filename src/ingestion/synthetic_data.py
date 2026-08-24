"""Curated benchmark dataset generator for SMS, Email, and URL branches.
Provides diverse real-world cyber threat patterns and benign communication baselines.
"""

import random
import pandas as pd
import numpy as np

# Seed for reproducibility
random.seed(42)
np.random.seed(42)

# ==========================================
# SMS Benchmark Generation
# ==========================================
SMS_SPAM_PATTERNS = [
    "URGENT: Your {bank} account has been suspended due to suspicious activity. Verify now at {url}",
    "WINNER! You have been selected for a £{amount} Walmart gift card. Text CLAIM to {phone} or click {url}",
    "FINAL NOTICE: IRS tax refund of ${amount} pending approval. Confirm identity immediately at {url}",
    "Alert: Unauthorized login attempt detected from IP {ip}. Secure your {service} account: {url}",
    "Congratulations! You won the European Lottery prize of £{amount}000. Contact claims officer at {email}",
    "Your package #{tracking} could not be delivered due to incorrect address. Update details: {url}",
    "FREE ENTRY: Win a weekly cash prize of ${amount}! Text GO to {phone} now. T&Cs apply.",
    "Bank Security: Your debit card ending in {digits} was charged ${amount}. If not you, visit {url} immediately.",
    "Netflix: We had trouble processing your billing information. Update payment within 24h: {url}",
    "Action Required: You have 1 unread secure voicemail from HR. Listen here: {url}",
    "Crypto Alert: {amount} BTC received in your wallet! Claim and withdraw now: {url}",
    "Geek Squad Renewal: $399 auto-deducted for annual protection. Call +1-800-{phone_suffix} to cancel.",
    "Your Apple ID has been locked for security reasons. Unlock at {url}",
    "IMPORTANT: COVID-19 relief fund deposit of ${amount} waiting. Claim before deadline: {url}",
    "CashApp: You received ${amount} from John. Accept payment here: {url}"
]

SMS_HAM_PATTERNS = [
    "Hey, are we still meeting for lunch at 12:30 today?",
    "Your appointment with Dr. Miller is confirmed for tomorrow at 3 PM.",
    "Hi mom, I just landed safely at the airport. Will call you soon.",
    "Your verification code for {service} is {otp}. Do not share this code.",
    "Can you please review the attached document before our team sync?",
    "Hey mate, don't forget to bring the projector for tomorrow's demo.",
    "Your Uber driver is arriving in 3 minutes in a Silver Toyota Camry.",
    "Thanks for dinner last night, had a wonderful time catching up!",
    "Reminder: Library books are due back by Friday afternoon.",
    "Hey! Are you coming to Sarah's birthday party this Saturday?",
    "Your order #{tracking} from Amazon has been delivered to your front door.",
    "Don't worry about the report, I already sent it over to Dave.",
    "Good morning! Let me know when you're free for a quick 5-min call.",
    "The groceries are on the counter, see you at home tonight.",
    "Your table reservation at Bistro Bella is confirmed for 7:30 PM."
]

BANKS = ["Chase", "Wells Fargo", "Bank of America", "CitiBank", "Barclays", "HSBC", "SBI"]
SERVICES = ["PayPal", "Apple", "Google", "Amazon", "Netflix", "Microsoft", "Coinbase"]
URLS = ["http://chase-update-security.xyz/login", "http://secure-paypal-verify.top", "http://appleid-unlock.ml", "http://bit.ly/claim-prize-382", "http://192.168.1.105/auth"]


def generate_benchmark_sms(n_samples: int = 1200) -> pd.DataFrame:
    """Generate a rich benchmark dataset of SMS spam and ham."""
    data = []
    
    # Generate Spam
    for _ in range(n_samples // 2):
        template = random.choice(SMS_SPAM_PATTERNS)
        text = template.format(
            bank=random.choice(BANKS),
            service=random.choice(SERVICES),
            url=random.choice(URLS),
            amount=random.randint(100, 5000),
            phone=f"{random.randint(80000, 89999)}",
            phone_suffix=f"{random.randint(1000, 9999)}",
            digits=f"{random.randint(1000, 9999)}",
            email="claims@award-central.com",
            tracking=f"US{random.randint(100000, 999999)}X",
            ip=f"{random.randint(11, 220)}.{random.randint(1, 250)}.{random.randint(1, 250)}.{random.randint(1, 250)}"
        )
        data.append({"text": text, "label": 1})

    # Generate Ham
    for _ in range(n_samples // 2):
        template = random.choice(SMS_HAM_PATTERNS)
        text = template.format(
            service=random.choice(SERVICES),
            otp=f"{random.randint(100000, 999999)}",
            tracking=f"AMZ{random.randint(10000, 99999)}"
        )
        data.append({"text": text, "label": 0})

    df = pd.DataFrame(data).sample(frac=1.0, random_state=42).reset_index(drop=True)
    return df


# ==========================================
# Email Benchmark Generation
# ==========================================
EMAIL_PHISHING_TEMPLATES = [
    "Subject: URGENT: Action Required on Your {service} Account\n\nDear Customer,\nWe detected multiple unauthorized login attempts to your account. For your protection, we have temporarily restricted access. To restore full access, please click the secure link below to verify your identity within 24 hours.\n\nLink: {url}\n\nFailure to verify will result in permanent account termination.\n\nSecurity Operations Team",
    "Subject: Invoice #{invoice_id} Payment Overdue - Final Warning\n\nAttention Accounts Payable,\nPlease find attached overdue invoice #{invoice_id} for services rendered in amount of ${amount}. If payment is not submitted immediately via our secure portal {url}, legal proceedings will commence.\n\nFinance Department",
    "Subject: Shared Document: Q3 Executive Compensation Review.pdf\n\nHi,\nI have shared a confidential document with you via DocuSign. Click here to view and sign: {url}\n\nThis document requires your immediate digital signature.",
    "Subject: Microsoft 365 Password Expiration Alert\n\nYour organization password will expire in 2 hours. Keep your current password by confirming credentials here: {url}\n\nIT Support Helpdesk",
    "Subject: PayPal: Suspicious Transaction of ${amount} to Bitcoin Exchange\n\nDear User,\nYou sent a payment of ${amount} USD to CryptoHub. If you did not authorize this payment, cancel the transaction immediately by clicking here: {url}",
    "Subject: Internal Payroll Direct Deposit Update\n\nAll employees must update their direct deposit banking details due to standard fiscal year maintenance. Complete your form here: {url}\n\nHuman Resources Department"
]

EMAIL_HAM_TEMPLATES = [
    "Subject: Weekly Project Status Update & Architecture Review\n\nHi Team,\nPlease find the meeting minutes from today's sprint review. We completed the API migration and will begin load testing next Tuesday. Let me know if you have any questions.\n\nBest regards,\nEngineering Team",
    "Subject: Invitation: Monthly All-Hands Meeting\n\nHello Everyone,\nPlease join us for our monthly all-hands meeting this Thursday at 2:00 PM EST. Agenda includes company performance, product roadmap updates, and Q&A session.",
    "Subject: GitHub: Pull Request #142 Merged into main\n\nYour pull request 'feat: add telemetry metrics to payment service' was approved and merged successfully. All CI/CD checks passed.",
    "Subject: Lunch & Learn: Introduction to Large Language Models\n\nHi all,\nJoin us in Conference Room B tomorrow at 12 PM for a presentation on transformer architectures and fine-tuning strategies. Lunch will be provided!",
    "Subject: AWS Billing Statement for Account #8392183\n\nYour monthly AWS invoice is now available in the AWS Management Console. Total charges for the billing period are $142.50.",
    "Subject: Out of Office: Traveling for Tech Conference\n\nI will be out of the office from Monday to Thursday attending PyCon. For urgent matters, please contact Sarah from the DevOps team."
]


def generate_benchmark_emails(n_samples: int = 1200) -> pd.DataFrame:
    """Generate a rich benchmark dataset of Phishing and Benign Emails."""
    data = []
    
    for _ in range(n_samples // 2):
        template = random.choice(EMAIL_PHISHING_TEMPLATES)
        text = template.format(
            service=random.choice(SERVICES),
            url=random.choice(URLS),
            invoice_id=f"INV-{random.randint(10000, 99999)}",
            amount=random.randint(450, 9800)
        )
        data.append({"text": text, "label": 1})

    for _ in range(n_samples // 2):
        template = random.choice(EMAIL_HAM_TEMPLATES)
        text = template
        data.append({"text": text, "label": 0})

    df = pd.DataFrame(data).sample(frac=1.0, random_state=42).reset_index(drop=True)
    return df


# ==========================================
# URL Benchmark Generation
# ==========================================
LEGIT_DOMAINS = [
    "google.com", "microsoft.com", "apple.com", "amazon.com", "github.com",
    "wikipedia.org", "nytimes.com", "cnn.com", "stackoverflow.com", "netflix.com",
    "chase.com", "bankofamerica.com", "paypal.com", "linkedin.com", "twitter.com",
    "spotify.com", "adobe.com", "dropbox.com", "cloudflare.com", "shopify.com"
]

MALICIOUS_DOMAINS_AND_PATHS = [
    # Typosquatting
    ("paypa1-security-login.xyz", "/auth/verify?session=92842"),
    ("micros0ft-support-portal.top", "/login.php?client=azure"),
    ("chase-bank-verify-account.click", "/secure/signin"),
    ("appleid-recover-account.ml", "/find-my-iphone/login"),
    ("wellsfarg0-online-banking.work", "/update-credentials"),
    ("netflix-billing-update.buzz", "/your-account/payment"),
    ("amzn-prime-rewards.top", "/claim?id=4928"),
    ("coinbase-wallet-security.xyz", "/app/login"),
    ("faceb00k-security-checkpoint.cf", "/checkpoint/?id=983"),
    ("docusign-sign-document.tk", "/docusign/view-envelope"),
    # IP as host
    ("192.168.1.105:8080", "/phishing/login.html"),
    ("185.220.101.4", "/bin/malware.exe"),
    ("45.142.214.12", "/admin/credential_stealer.php"),
    # Generic malicious TLD & long path
    ("free-giftcard-generator.xyz", "/win/iphone15/claim.php?ref=spam"),
    ("secure-banking-update-notice.top", "/client/portal/auth"),
    ("update-tax-refund-portal.click", "/irs/gov/refund_process.html")
]

LEGIT_PATHS = [
    "/", "/about", "/contact-us", "/products/software", "/docs/getting-started",
    "/blog/engineering-updates", "/search?q=machine+learning", "/help/article/392",
    "/pricing", "/solutions/enterprise", "/news/2026/04/tech-announcement"
]


def generate_benchmark_urls(n_samples: int = 1500) -> pd.DataFrame:
    """Generate a rich benchmark dataset of Benign and Malicious URLs with realistic domain clusters."""
    data = []

    # Benign URLs
    for _ in range(n_samples // 2):
        domain = random.choice(LEGIT_DOMAINS)
        path = random.choice(LEGIT_PATHS)
        protocol = "https://" if random.random() > 0.1 else "http://"
        url = f"{protocol}www.{domain}{path}"
        data.append({"url": url, "label": 0})

    # Malicious URLs
    for _ in range(n_samples // 2):
        domain, path = random.choice(MALICIOUS_DOMAINS_AND_PATHS)
        protocol = "http://" if random.random() > 0.3 else "https://"
        url = f"{protocol}{domain}{path}"
        data.append({"url": url, "label": 1})

    df = pd.DataFrame(data).sample(frac=1.0, random_state=42).reset_index(drop=True)
    return df
