import redis
import re
from Redis.constants import TEXT_QUEUE, RESULT_LIST, INSULT_LIST
from Redis.insults_data import add_insult, get_insults

r = redis.Redis(decode_responses=True)

r.delete(TEXT_QUEUE)
r.delete(RESULT_LIST)
r.delete(INSULT_LIST)

insults = ["tonto", "idiota", "imbécil", "bobo", "cretino"]
for insult in insults:
    add_insult(insult)

texts = [
    "Mi jefe es un tonto.",
    "Ese conductor idiota casi me atropella.",
    "No seas tan imbécil.",
    "El profesor es un bobo.",
    "Nada especial hoy."  # sense insult
]

for text in texts:
    r.rpush(TEXT_QUEUE, text)
    print(f"[Producer] Enviat: {text}")

print("\n[Worker] Processant textos...")
while r.llen(TEXT_QUEUE) > 0:
    _, text = r.blpop(TEXT_QUEUE)
    insults = get_insults()
    filtered = text
    for insult in insults:
        pattern = re.compile(r'\b' + re.escape(insult) + r'\b', re.IGNORECASE)
        filtered = pattern.sub("CENSORED", filtered)
    r.rpush(RESULT_LIST, filtered)
    print(f"[Worker] Resultat: {filtered}")

print("\n[Viewer] Resultats filtrats:")
results = r.lrange(RESULT_LIST, 0, -1)
for result in results:
    print(f" - {result}")

if any("CENSORED" in res for res in results):
    print("\n✅ Test passat: s’han censurat insults.")
else:
    print("\n❌ Test fallat: cap insult censurat.")
