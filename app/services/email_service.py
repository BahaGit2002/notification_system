import aiosmtplib
from email.mime.text import MIMEText
from app.services.base import AsyncNotificationService
from app.config import EMAIL_FROM, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS


class EmailService(AsyncNotificationService):
    async def send(self, to: str, message: str) -> bool:
        try:
            msg = MIMEText(message)
            msg["Subject"] = "Notification"
            msg["From"] = EMAIL_FROM
            msg["To"] = to

            await aiosmtplib.send(
                msg,
                hostname=SMTP_HOST,
                port=SMTP_PORT,
                username=SMTP_USER,
                password=SMTP_PASS,
                start_tls=True
            )
            return True
        except Exception as e:
            print(f"[EMAIL] Error: {e}")
            return False
