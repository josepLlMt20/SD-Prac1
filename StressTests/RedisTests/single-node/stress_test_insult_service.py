import redis
import time
from StressTests.data_manager import guardar_resultats

r = redis.Redis(decode_responses=True)
NUM_INSULTS = 300

print(f"[STRESS TEST] Enviant {NUM_INSULTS} insults a la cua...")

start = time.time()

for i in range(NUM_INSULTS):
    insult = f"Generated insult #{i}"
    r.rpush("insult_queue", insult)

end = time.time()
duration = end - start
rps = NUM_INSULTS / duration

print(f"\n📊 Resultats:")
print(f" - Temps total: {duration:.2f}s")
print(f" - RPS (requests/second): {rps:.2f}")

data = [{
    "Test": "InsultService",
    "Middleware": "Redis",
    "Mode": "Single-node",
    "Clients": 1,
    "Num Tasks": NUM_INSULTS,
    "Temps Total (s)": round(duration, 2),
    "RPS": round(rps, 2)
}]

guardar_resultats(data, sheet_name="Redis_Single_Service")
