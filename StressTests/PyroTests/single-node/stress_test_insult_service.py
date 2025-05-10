import Pyro4
import time

NUM_INSULTS = 300

print(f"[PYRO STRESS TEST] Enviant {NUM_INSULTS} insults...")

insult_service = Pyro4.Proxy("PYRONAME:InsultService")

start_time = time.time()

for i in range(NUM_INSULTS):
    insult = f"Insult-{i}"
    insult_service.add_insult(insult)
    print(f"Text Afegit: {insult}")

end_time = time.time()
duration = end_time - start_time
rps = NUM_INSULTS / duration

print(f"\n📊 Resultats Pyro Insult Adder (Single-node):")
print(f" - Temps total: {duration:.2f}s")
print(f" - RPS (requests/second): {rps:.2f}")