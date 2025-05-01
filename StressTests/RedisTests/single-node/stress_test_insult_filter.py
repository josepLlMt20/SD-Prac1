import redis
import time
import re
import random
from Redis.constants import TEXT_QUEUE, RESULT_LIST, INSULT_LIST
from Redis.insults_data import add_insult, get_insults

r = redis.Redis(decode_responses=True)
NUM_TASKS = 300

r.delete(TEXT_QUEUE)
r.delete(RESULT_LIST)
r.delete(INSULT_LIST)

insults = ["tonto", "idiota", "imbécil", "bobo", "cretino"]
for insult in insults:
    add_insult(insult)

subjects = ["My boss", "The driver", "My coworker", "That guy", "The teacher"]
actions = ["is a", "acts like a", "behaves like a", "sounds like a", "looks like a"]

for _ in range(NUM_TASKS):
    subj = random.choice(subjects)
    insult = random.choice(insults)
    act = random.choice(actions)
    text = f"{subj} {act} {insult}."
    r.rpush(TEXT_QUEUE, text)

start = time.time()

count = 0
while count < NUM_TASKS:
    _, text = r.blpop(TEXT_QUEUE)
    insults = get_insults()
    filtered = text
    for insult in insults:
        pattern = re.compile(r'\b' + re.escape(insult) + r'\b', re.IGNORECASE)
        filtered = pattern.sub("CENSORED", filtered)
    r.rpush(RESULT_LIST, filtered)
    count += 1

end = time.time()
duration = end - start
rps = NUM_TASKS / duration

print("\n📊 Resultats del stress test:")
print(f" - Total textos processats: {NUM_TASKS}")
print(f" - Temps total: {duration:.2f} s")
print(f" - RPS (requests/second): {rps:.2f}")
