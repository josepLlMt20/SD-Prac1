import redis
import time
from Redis.insults_data import get_insults
from Redis.constants import INSULT_CHANNEL

# Publica insults del llistat
r = redis.Redis(decode_responses=True)

print("InsultBroadcaster corrent.")

while True:
    insults = get_insults()  # refresquem la llista a cada bucle
    if not insults:
        print("No hi ha insults disponibles.")
        time.sleep(5)
        continue

    for insult in insults:
        r.publish(INSULT_CHANNEL, insult)
        print(f"Insult publicat: {insult}")
        time.sleep(5)

