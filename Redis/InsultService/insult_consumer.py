import redis
from Redis.constants import INSULT_QUEUE
from Redis.insults_data import add_insult

# Guarda els insults rebus si no existeixen

r = redis.Redis(decode_responses=True)

print("InsultConsumer waiting for insults...")
while True:
    _, insult = r.blpop(INSULT_QUEUE)
    if add_insult(insult):
        print(f"Stored new insult: {insult}")
    else:
        print(f"Ignored duplicate insult: {insult}")
