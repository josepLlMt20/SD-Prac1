import Pyro4
import time
import random

NUM_TEXTS = 300

print(f"[STRESS TEST PYRO FILTER] Filtrant {NUM_TEXTS} textos...")

filter_service = Pyro4.Proxy("PYRONAME:FilterService")

insults = ["pedorro", "cabezón", "tontaco", "paco", "picapollo"]
subjects = ["Mi jefe", "Ese tipo", "Tu primo", "El informático", "Josep"]
actions = ["es un", "parece un", "se comporta como", "claramente es un"]

start_time = time.time()

for _ in range(NUM_TEXTS):
    text = f"{random.choice(subjects)} {random.choice(actions)} {random.choice(insults)}"
    filtered_text = filter_service.filter(text)
    print(f"Text filtrat: {filtered_text}")

end_time = time.time()
duration = end_time - start_time
rps = NUM_TEXTS / duration

print(f"\n📊 Resultats Pyro Filter (Single-node):")
print(f" - Temps total: {duration:.2f}s")
print(f" - RPS (requests/second): {rps:.2f}")