import redis
from Redis.constants import TEXT_QUEUE, RESULT_LIST, INSULT_LIST

r = redis.Redis(decode_responses=True)

r.delete(TEXT_QUEUE)
r.delete(RESULT_LIST)
r.delete(INSULT_LIST)

print("✅ Redis net.")
