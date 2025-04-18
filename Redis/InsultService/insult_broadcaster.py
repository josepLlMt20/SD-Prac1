import redis
import time
from Redis.insults_data import get_insults
from Redis.constants import INSULT_CHANNEL

# Publica insults del llistat

r = redis.Redis(decode_responses=True)

print("InsultBroadcaster started.")
while True:
    insults = get_insults()
    if insults:
        insult = insults[0]
        r.publish(INSULT_CHANNEL, insult)
        print(f"Broadcasted: {insult}")
    time.sleep(5)
