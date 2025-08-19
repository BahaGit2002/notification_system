import logging
from arq.connections import RedisSettings

from app.services.email_service import EmailService
from app.services.sms_service import SMSService
from app.services.telegram_service import TelegramService

logger = logging.getLogger("notification")
logging.basicConfig(level=logging.INFO)
channel_to_field = {
    "telegram": "telegram_id",
    "email": "email",
    "sms": "phone"
}
services = {
    "email": EmailService(),
    "sms": SMSService(),
    "telegram": TelegramService(),
}


async def send_notification(ctx, notification: dict):
    message = notification["message"]
    for channel in notification["channels_priority"]:
        field = channel_to_field.get(channel)
        target = notification.get(field)
        if not target:
            continue
        success = await services[channel].send(target, message)
        if success:
            logger.info(f"[OK] Delivered via {channel}")
            return True
        else:
            logger.warning(f"[FAIL] {success}, try next…")
    return False


class WorkerSettings:
    functions = [send_notification]
    redis_settings = RedisSettings(host="redis", port=6379)
