import xmlrpc.client
import time
import threading
import re
import random
from StressTests.data_manager import guardar_resultats

NUM_TASKS = 300
TEXTS = [
    "Eres un tonto integral.",
    "Mi jefe es un cretino.",
    "Hoy he hablado con un idiota.",
    "Qué bobo eres a veces.",
    "Nada especial hoy.",
]

INSULTS = ["tonto", "idiota", "imbécil", "bobo", "cretino"]

def worker_loop(n):
    proxy = xmlrpc.client.ServerProxy("http://localhost:8010/")  # Proxy per cada worker
    count = 0
    while True:
        try:
            text = proxy.get_task()
            if not text:
                break
            insults = proxy.get_insults()
            filtered = text
            for insult in insults:
                pattern = re.compile(r'\b' + re.escape(insult) + r'\b', re.IGNORECASE)
                filtered = pattern.sub("CENSORED", filtered)
            proxy.submit_result(filtered)
            count += 1
        except Exception as e:
            print(f"[Worker-{n}] Error: {e}")
            break
    print(f"[Worker-{n}] Processed {count} tasks.")

def run_scaling_test(num_workers):
    print(f"\n Testing amb {num_workers} worker(s)...")

    # Reiniciem estat del servidor
    reset_proxy = xmlrpc.client.ServerProxy("http://localhost:8010/")
    reset_proxy.reset()

    # Afegim insults
    for insult in INSULTS:
        reset_proxy.submit_insult(insult)

    # Enviem textos
    for _ in range(NUM_TASKS):
        reset_proxy.submit_text(random.choice(TEXTS))

    threads = []
    start = time.time()

    for i in range(num_workers):
        t = threading.Thread(target=worker_loop, args=(i + 1,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    end = time.time()
    duration = end - start
    print(f"⏱ Temps total: {duration:.2f}s")
    return duration

if __name__ == "__main__":
    results = []
    for workers in [1, 2, 3]:
        duration = run_scaling_test(workers)
        results.append((workers, duration))

    print("\n Resultats finals:")
    for workers, dur in results:
        print(f"{workers} workers ➝ {dur:.2f}s")

    speedup_1 = results[0][1]
    for workers, dur in results[1:]:
        speedup = speedup_1 / dur
        print(f" Speedup amb {workers} workers: {speedup:.2f}x")

    data = []
    for clients, duration in results:
        speedup = baseline / duration if clients > 1 else 1.0
        data.append({
            "Test": "InsultFilter",
            "Middleware": "XMLRPC",
            "Mode": "Multi-node",
            "Clients": clients,
            "Num Tasks": NUM_TASKS,
            "Temps Total (s)": round(duration, 2),
            "Speedup": round(speedup, 2)
        })

    guardar_resultats(data, sheet_name="XMLRPC_Multi_Filter")
