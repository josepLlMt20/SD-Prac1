import redis
import time
from Redis.constants import INSULT_QUEUE

# Envia insults a la cua cada 5 segons

r = redis.Redis(decode_responses=True)

insults = [
    "You're as useless as the 'ueue' in 'queue'.",
    "You bring everyone joy… when you leave the room.",
    "You're the reason the gene pool needs a lifeguard."
]

i = 0
while True:
    insult = insults[i % len(insults)]
    r.rpush(INSULT_QUEUE, insult)
    print(f"Produced: {insult}")
    i += 1
    time.sleep(5)
