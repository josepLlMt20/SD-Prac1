import Pyro4
import time
from StressTests.data_manager import guardar_resultats

NUM_INSULTS = 1000

print(f"[PYRO STRESS TEST] Enviant {NUM_INSULTS} insults...")

insult_service = Pyro4.Proxy("PYRONAME:InsultService1")

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

data = [{
    "Test": "InsultService",
    "Middleware": "PyRO",
    "Mode": "Single-node",
    "Clients": 1,
    "Num Tasks": NUM_INSULTS,
    "Temps Total (s)": round(duration, 2),
    "RPS": round(rps, 2)
}]

guardar_resultats(data, sheet_name="PyRO_Single_Service")