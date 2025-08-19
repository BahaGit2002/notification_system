import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")

EMAIL_FROM = os.getenv("EMAIL_FROM", "noreply@example.com")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.example.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "user")
SMTP_PASS = os.getenv("SMTP_PASS", "password")

SMS_API_URL = os.getenv("SMS_API_URL", "https://sms-provider/api")
SMS_API_KEY = os.getenv("SMS_API_KEY", "fake-key")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "fake-token")
