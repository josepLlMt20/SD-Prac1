import redis
from Redis.constants import TEXT_QUEUE, RESULT_LIST
from Redis.insults_data import get_insults

# Filtra els insults desl texts i guarda la resta

r = redis.Redis(decode_responses=True)

print("InsultFilter worker started.")
while True:
    _, text = r.blpop(TEXT_QUEUE)
    insults = get_insults()
    filtered = text
    for insult in insults:
        filtered = filtered.replace(insult, "CENSORED")
    r.rpush(RESULT_LIST, filtered)
    print(f"Filtered text: {filtered}")
