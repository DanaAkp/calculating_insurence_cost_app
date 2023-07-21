import datetime

from redis.asyncio import Redis
from redis.asyncio.utils import from_url

from app.config import REDIS_PORT, REDIS_HOST


class Service:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def set(self, key: str, values: str) -> None:
        now = datetime.datetime.now()
        half_night = datetime.datetime(now.year, now.month, now.day + 1)
        await self._redis.set(name=key, value=values, ex=half_night - now)

    async def get(self, key: str) -> str:
        return await self._redis.get(name=key)


service = Service(from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf-8", decode_responses=True))
