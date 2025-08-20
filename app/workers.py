import logging
from arq.connections import RedisSettings

from app.services.email_service import EmailService
from app.services.sms_service import SMSService
from app.services.telegram_service import TelegramService

logger = logging.getLogger("notification")

channel_to_field = {
    "telegram": "telegram_id",
    "email": "email",
    "sms": "phone"
}


async def send_notification(ctx, notification: dict):
    message = notification["message"]

    for channel in notification["channels_priority"]:
        field = channel_to_field.get(channel)
        target = notification.get(field)
        if not target:
            continue

        try:
            service = ctx["services"][channel]
            success = await service.send(target, message)
        except Exception as e:
            logger.error(f"[ERROR] {channel} failed: {e}")
            success = False

        if success:
            logger.info(f"[OK] Delivered via {channel}")
            return True
        else:
            logger.warning(f"[FAIL] via {channel}, try next…")

    logger.error("Не удалось доставить уведомление")
    return False


async def startup(ctx):
    ctx["services"] = {
        "email": EmailService(),
        "sms": SMSService(),
        "telegram": TelegramService(),
    }


class WorkerSettings:
    functions = [send_notification]
    redis_settings = RedisSettings(host="redis", port=6379)
    on_startup = startup
