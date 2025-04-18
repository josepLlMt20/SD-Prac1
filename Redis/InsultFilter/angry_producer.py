import redis
import time
from Redis.constants import TEXT_QUEUE

# Genera texts amb insults cada 5 segons

r = redis.Redis(decode_responses=True)

angry_lines = [
    "You're as useless as the 'ueue' in 'queue'.",
    "I can't believe you wrote this code."
]

i = 0
while True:
    text = f"Here’s some angry input: {angry_lines[i % len(angry_lines)]}"
    r.rpush(TEXT_QUEUE, text)
    print(f"Produced (angry): {text}")
    i += 1
    time.sleep(5)
