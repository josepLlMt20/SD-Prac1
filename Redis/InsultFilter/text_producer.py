import redis
import time
from Redis.constants import TEXT_QUEUE

# Envia text normal a la cua cada 5 segons

r = redis.Redis(decode_responses=True)

i = 0
while True:
    text = f"This is a clean text message number {i}."
    r.rpush(TEXT_QUEUE, text)
    print(f"Produced (clean): {text}")
    i += 1
    time.sleep(5)
