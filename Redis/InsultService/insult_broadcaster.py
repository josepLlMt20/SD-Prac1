import redis
import time
from Redis.insults_data import get_insults
from Redis.constants import INSULT_CHANNEL

# Publica insults del llistat
r = redis.Redis(decode_responses=True)

print("InsultBroadcaster started.")

while True:
    insults = get_insults()  # refresquem la llista a cada bucle
    if not insults:
        print("No insults available.")
        time.sleep(5)
        continue

    for insult in insults:
        r.publish(INSULT_CHANNEL, insult)
        print(f"Broadcasted: {insult}")
        time.sleep(5)

