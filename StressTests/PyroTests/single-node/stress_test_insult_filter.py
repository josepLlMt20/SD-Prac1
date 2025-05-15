import Pyro4
import time
import random
from StressTests.data_manager import guardar_resultats

NUM_TEXTS = 1000

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

data = [{
    "Test": "InsultFilter",
    "Middleware": "PyRO",
    "Mode": "Single-node",
    "Clients": 1,
    "Num Tasks": NUM_TEXTS,
    "Temps Total (s)": round(duration, 2),
    "RPS": round(rps, 2)
}]

guardar_resultats(data, sheet_name="PyRO_Single_Filter")