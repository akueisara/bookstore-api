import aioredis
from utils.const import TESTING, REDIS_URL

redis = None


async def check_test_redis():
    global redis
    if TESTING:
        redis = await aioredis.create_redis_pool(REDIS_URL)
