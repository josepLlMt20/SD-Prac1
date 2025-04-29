import xmlrpc.client
import time
import random
import re
from threading import Thread

proxy = xmlrpc.client.ServerProxy("http://localhost:8010/")
NUM_REQUESTS = 250

# Afegim insults
insults = ["tonto", "idiota", "imbécil", "bobo", "cretino"]
for insult in insults:
    proxy.submit_insult(insult)

texts = [
    "Eres un tonto integral.",
    "Mi jefe es un cretino.",
    "Hoy he hablado con un idiota.",
    "Qué bobo eres a veces.",
    "Nada especial hoy.",
]

def run_worker(stop_after):
    processed = 0
    while processed < stop_after:
        text = proxy.get_task()
        if not text:
            time.sleep(0.01)
            continue
        insult_list = proxy.get_insults()
        filtered = text
        for insult in insult_list:
            pattern = re.compile(r'\b' + re.escape(insult) + r'\b', re.IGNORECASE)
            filtered = pattern.sub("CENSORED", filtered)
        proxy.submit_result(filtered)
        processed += 1

# Llançar el worker
worker_thread = Thread(target=run_worker, args=(NUM_REQUESTS,))
worker_thread.start()

print(f"[STRESS TEST] Enviant {NUM_REQUESTS} textos...")
start_time = time.time()

for i in range(NUM_REQUESTS):
    proxy.submit_text(random.choice(texts))

end_time = time.time()
worker_thread.join()

duration = end_time - start_time
rps = NUM_REQUESTS / duration

print(f"\n📊 Resultats:")
print(f" - Temps total: {duration:.2f} s")
print(f" - RPS (Requests per second): {rps:.2f}")
