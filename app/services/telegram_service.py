import httpx
from app.services.base import AsyncNotificationService
from app.config import TELEGRAM_BOT_TOKEN


class TelegramService(AsyncNotificationService):
    async def send(self, to: str, message: str) -> bool:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    url, data={"chat_id": to, "text": message}
                )
            return resp.status_code == 200
        except Exception as e:
            print(f"[TELEGRAM] Error: {e}")
            return False
