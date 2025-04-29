import xmlrpc.client
import time

NUM_REQUESTS = 250
proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

print(f"[STRESS TEST] Enviant {NUM_REQUESTS} insults...")

start_time = time.time()

for i in range(NUM_REQUESTS):
    proxy.add_insult(f"insult-{i}")

end_time = time.time()
duration = end_time - start_time
rps = NUM_REQUESTS / duration

print(f"\n📊 Resultats del stress test:")
print(f" - Temps total: {duration:.2f} s")
print(f" - RPS (Requests per second): {rps:.2f}")
