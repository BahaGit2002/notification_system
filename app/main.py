import logging

from fastapi import FastAPI
from app.schemas import NotificationRequest
from arq.connections import RedisSettings, create_pool
from urllib.parse import urlparse

from app.config import REDIS_URL

logger = logging.getLogger("notification")
url = urlparse(REDIS_URL)


redis_settings = RedisSettings(
    host=url.hostname,
    port=url.port,
    password=url.password,
    database=int(url.path.lstrip('/')) if url.path else 0
)

app = FastAPI()


@app.on_event("startup")
async def startup():
    app.state.redis = await create_pool(redis_settings)
    logger.info("Redis pool created")


@app.on_event("shutdown")
async def shutdown():
    await app.state.redis.close()
    logger.info("Redis pool closed")


@app.post("/notify/")
async def notify(data: NotificationRequest):
    payload = data.model_dump()
    await app.state.redis.enqueue_job("send_notification", payload)
    return {"status": "queued"}
