import httpx
from app.services.base import AsyncNotificationService
from app.config import SMS_API_URL, SMS_API_KEY


class SMSService(AsyncNotificationService):
    async def send(self, to: str, message: str) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    SMS_API_URL,
                    json={"to": to, "text": message, "api_key": SMS_API_KEY},
                    timeout=10
                )
            return resp.status_code == 200
        except Exception as e:
            print(f"[SMS] Error: {e}")
            return False
