import redis
import time
from Redis.constants import INSULT_QUEUE, INSULT_LIST, INSULT_CHANNEL

r = redis.Redis(decode_responses=True)

print("[TEST] Començant test funcional Redis InsultService")

# Netejar dades prèvies
r.delete(INSULT_QUEUE)
r.delete(INSULT_LIST)

# Enviar insults a la cua
sample_insults = [
    "You code like it's still 1999.",
    "You're a merge conflict personified.",
    "You make off-by-one errors... on purpose."
]

print("[TEST] Enviant insults a la cua...")
for insult in sample_insults:
    r.rpush(INSULT_QUEUE, insult)
    print(f" - Enviat: {insult}")

# Esperar perquè el `insult_consumer.py` els processi
print("[TEST] Esperant que el consumer els processi...")
time.sleep(5)

# Validar si s'han desat al set
stored_insults = r.smembers(INSULT_LIST)
print(f"[TEST] Insults desats: {len(stored_insults)}")
for insult in stored_insults:
    print(f" - {insult}")

# Enviar broadcast
print("[TEST] Publicant insults...")
for insult in stored_insults:
    r.publish(INSULT_CHANNEL, insult)
    print(f" - Broadcasted: {insult}")

print("\n✅ Test completat (comprova consola de `insult_receiver.py`).")