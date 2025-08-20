import pytest
from unittest.mock import AsyncMock, MagicMock
from app.workers import send_notification, startup
from app.services.email_service import EmailService
from app.services.sms_service import SMSService
from app.services.telegram_service import TelegramService


@pytest.mark.asyncio
async def test_send_notification_success_email(mocker):
    ctx = {
        "services": {
            "email": AsyncMock(spec=EmailService),
            "sms": AsyncMock(spec=SMSService),
            "telegram": AsyncMock(spec=TelegramService)
        }
    }

    ctx["services"]["email"].send.return_value = True

    notification = {
        "message": "Тестовое сообщение",
        "channels_priority": ["email", "sms", "telegram"],
        "email": "test@example.com",
        "phone": "+1234567890",
        "telegram_id": "123456"
    }

    mock_logger = mocker.patch("app.workers.logger", new=MagicMock())

    result = await send_notification(ctx, notification)

    assert result is True
    ctx["services"]["email"].send.assert_called_once_with(
        "test@example.com", "Тестовое сообщение"
    )
    ctx["services"]["sms"].send.assert_not_called()
    ctx["services"]["telegram"].send.assert_not_called()
    mock_logger.info.assert_called_with("[OK] Delivered via email")


@pytest.mark.asyncio
async def test_send_notification_fallback_to_sms(mocker):
    ctx = {
        "services": {
            "email": AsyncMock(spec=EmailService),
            "sms": AsyncMock(spec=SMSService),
            "telegram": AsyncMock(spec=TelegramService)
        }
    }

    ctx["services"]["email"].send.return_value = False
    ctx["services"]["sms"].send.return_value = True

    notification = {
        "message": "Тестовое сообщение",
        "channels_priority": ["email", "sms", "telegram"],
        "email": "test@example.com",
        "phone": "+1234567890",
        "telegram_id": "123456"
    }

    mock_logger = mocker.patch("app.workers.logger", new=MagicMock())

    result = await send_notification(ctx, notification)

    assert result is True
    ctx["services"]["email"].send.assert_called_once_with(
        "test@example.com", "Тестовое сообщение"
    )
    ctx["services"]["sms"].send.assert_called_once_with(
        "+1234567890", "Тестовое сообщение"
    )
    ctx["services"]["telegram"].send.assert_not_called()
    mock_logger.warning.assert_called_with("[FAIL] via email, try next…")
    mock_logger.info.assert_called_with("[OK] Delivered via sms")


@pytest.mark.asyncio
async def test_send_notification_all_channels_fail(mocker):
    ctx = {
        "services": {
            "email": AsyncMock(spec=EmailService),
            "sms": AsyncMock(spec=SMSService),
            "telegram": AsyncMock(spec=TelegramService)
        }
    }

    # Настраиваем заглушки: все каналы неуспешны
    ctx["services"]["email"].send.return_value = False
    ctx["services"]["sms"].send.return_value = False
    ctx["services"]["telegram"].send.return_value = False

    notification = {
        "message": "Тестовое сообщение",
        "channels_priority": ["email", "sms", "telegram"],
        "email": "test@example.com",
        "phone": "+1234567890",
        "telegram_id": "123456"
    }

    mock_logger = mocker.patch("app.workers.logger", new=MagicMock())

    result = await send_notification(ctx, notification)

    assert result is False
    ctx["services"]["email"].send.assert_called_once_with(
        "test@example.com", "Тестовое сообщение"
    )
    ctx["services"]["sms"].send.assert_called_once_with(
        "+1234567890", "Тестовое сообщение"
    )
    ctx["services"]["telegram"].send.assert_called_once_with(
        "123456", "Тестовое сообщение"
    )
    mock_logger.error.assert_called_with("Не удалось доставить уведомление")


@pytest.mark.asyncio
async def test_send_notification_missing_target(mocker):
    ctx = {
        "services": {
            "email": AsyncMock(spec=EmailService),
            "sms": AsyncMock(spec=SMSService),
            "telegram": AsyncMock(spec=TelegramService)
        }
    }

    notification = {
        "message": "Тестовое сообщение",
        "channels_priority": ["email", "sms", "telegram"],
    }

    mock_logger = mocker.patch("app.workers.logger", new=MagicMock())

    result = await send_notification(ctx, notification)

    assert result is False
    ctx["services"]["email"].send.assert_not_called()
    ctx["services"]["sms"].send.assert_not_called()
    ctx["services"]["telegram"].send.assert_not_called()
    mock_logger.error.assert_called_with("Не удалось доставить уведомление")


@pytest.mark.asyncio
async def test_startup():
    ctx = {}
    await startup(ctx)

    assert "services" in ctx
    assert isinstance(ctx["services"]["email"], EmailService)
    assert isinstance(ctx["services"]["sms"], SMSService)
    assert isinstance(ctx["services"]["telegram"], TelegramService)
