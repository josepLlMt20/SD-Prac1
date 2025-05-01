import redis
from Redis.constants import TEXT_QUEUE, RESULT_LIST
from Redis.insults_data import get_insults
import re

# Filtra els insults desl texts i guarda la resta

r = redis.Redis(decode_responses=True)

print("InsultFilter worker corrent.")
while True:
    _, text = r.blpop(TEXT_QUEUE)
    insults = get_insults()
    filtered = text
    for insult in insults:
        pattern = re.compile(r'\b' + re.escape(insult) + r'\b', re.IGNORECASE)
        filtered = pattern.sub("CENSORED", filtered)
    r.rpush(RESULT_LIST, filtered)
    print(f"Text filtrat: {filtered}")
