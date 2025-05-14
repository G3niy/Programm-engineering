import redis
from redis.asyncio import Redis
import os
import json

class RedisCache:
    def __init__(self):
        self.redis = None

    async def get_redis(self) -> Redis:
        if self.redis is None:
            REDIS_URL = os.getenv("REDIS_URL", "redis://cache:6379/0")
            self.redis = Redis.from_url(REDIS_URL, decode_responses=True)
        return self.redis

    async def cache_task(self, service: dict, ttl: int = 86400000):
        redis = await self.get_redis()
        service_id = service.get("code")
        value = json.dumps(service)

        await redis.setex(
            f"{service_id}",
            ttl,
            value
        )

    async def get_service(self, service_id: str) -> dict | None:
        redis = await self.get_redis()
        key = f"{service_id}"
        service = await redis.get(key)
        return json.loads(service) if service else None

    async def del_service(self, service_id: str):
        redis = await self.get_redis()
        await redis.delete(f"{service_id}")

    async def close(self):
        if self.redis and not self.redis.closed:
            await self.redis.close()
