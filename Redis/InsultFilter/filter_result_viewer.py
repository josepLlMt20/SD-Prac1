import redis
from Redis.constants import RESULT_LIST

# Mostra els texts ja filtrats

r = redis.Redis(decode_responses=True)

results = r.lrange(RESULT_LIST, 0, -1)
print("Filtered results:")
for result in results:
    print(f"- {result}")
