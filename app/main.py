from fastapi import FastAPI
from app.schemas import NotificationRequest
from arq.connections import RedisSettings, create_pool
from urllib.parse import urlparse

from app.config import REDIS_URL

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


@app.post("/notify/")
async def notify(data: NotificationRequest):
    await app.state.redis.enqueue_job("send_notification", data.dict())
    return {"status": "queued"}
