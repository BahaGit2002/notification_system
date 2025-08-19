# Async Notification System

Система уведомлений на FastAPI с асинхронной отправкой через Email, SMS и Telegram.
Использует ARQ для очередей задач и Redis для хранения задач.

---

## 🚀 Особенности

* Асинхронная отправка уведомлений.
* Поддержка нескольких каналов: Email, SMS, Telegram.
* Приоритет каналов: если один не сработал, пробует следующий.
* Логирование доставки уведомлений.
* Подключение к Redis для очередей задач.
* Можно расширять другими каналами уведомлений.

---

## 📦 Технологии

* Python 3.11
* FastAPI
* ARQ
* Redis
* Async HTTP (httpx)
* PostgreSQL (для логирования уведомлений)
* Docker & Docker Compose

---

## ⚙️ Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/BahaGit2002/notification_system
cd notification_system
```

2. Создайте `.env` файл с переменными:

```env
REDIS_URL=redis://redis:6379/0
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASS=
EMAIL_FROM=
TELEGRAM_BOT_TOKEN=
SMS_API_URL=dummy
SMS_API_KEY=api_key
```

3. Соберите и запустите Docker контейнеры:

```bash
docker-compose up --build
```

---

## 📌 Использование

### Отправка уведомления

POST-запрос на `/notify/`:

```json
{
  "user_id": 1,
  "email": "user@example.com",
  "phone": "+123456789",
  "telegram_id": "6860846832",
  "message": "Привет! Это тестовое уведомление",
  "channels_priority": ["telegram", "email", "sms"]
}
```

* `channels_priority` — список каналов в порядке приоритета.
* Система попытается доставить уведомление по каждому каналу, пока не добьётся успеха.

---

### Пример cURL

```bash
curl -X POST http://localhost:8000/notify/ \
-H "Content-Type: application/json" \
-d '{
  "user_id": 1,
  "email": "user@example.com",
  "phone": "+123456789",
  "telegram_id": "6860846832",
  "message": "Привет! Это тестовое уведомление 👋",
  "channels_priority": ["telegram", "email", "sms"]
}'
```

---

## 📋 Структура проекта

```
app/
├─ main.py              # FastAPI приложение
├─ workers.py           # ARQ воркер
├─ services/
│  ├─ base.py           # базовый класс AsyncNotificationService
│  ├─ telegram_service.py
│  ├─ email_service.py
│  └─ sms_service.py
├─ schemas.py           # Pydantic схемы
├─ config.py            # Конфигурации (Redis, Telegram, Email)
```

---

## 📝 Логи и отладка

* В воркере используйте logging для проверки доставки:

```python
import logging
logger = logging.getLogger("notification")
logger.info("Notification sent")
```

* Для просмотра логов в Docker:

```bash
docker-compose logs -f worker
```

---

## ⚠️ Важные заметки

* Для Telegram: пользователь **должен написать боту хотя бы один раз**. Иначе сообщение не доставится.
* SMS может быть платным в зависимости от провайдера.
* Email требует корректного SMTP-конфига.

---

## 🔧 Расширение

* Добавление новых каналов уведомлений легко через создание нового сервиса, наследуемого от `AsyncNotificationService`.
* Можно добавить логирование каждой попытки в PostgreSQL.

---

## 📚 Литература

* [FastAPI Documentation](https://fastapi.tiangolo.com/)
* [ARQ Documentation](https://arq-docs.helpmanual.io/)
* [Telegram Bot API](https://core.telegram.org/bots/api)
