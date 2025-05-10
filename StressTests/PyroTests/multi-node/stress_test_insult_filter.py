import Pyro4
import time
import threading
import random
from StressTests.data_manager import guardar_resultats

NUM_TEXTS = 300

def filter_texts(client_id, texts_to_filter):
    filter_service = Pyro4.Proxy("PYRONAME:FilterService")
    insults = ["pedorro", "cabezón", "tontaco", "paco", "picapollo"]
    subjects = ["Mi jefe", "Ese tipo", "Tu primo", "El informático", "Josep"]
    actions = ["es un", "parece un", "se comporta como", "claramente es un"]

    for _ in range(texts_to_filter):
        text = f"{random.choice(subjects)} {random.choice(actions)} {random.choice(insults)}"
        filtered_text = filter_service.filter(text)
        print(f"[Client-{client_id}] Text filtrat: {filtered_text}")

def run_scaling_test(num_clients):
    print(f"\nTest amb {num_clients} client(s)...")
    threads = []
    texts_per_client = NUM_TEXTS // num_clients
    start_time = time.time()

    for i in range(num_clients):
        t = threading.Thread(target=filter_texts, args=(i + 1, texts_per_client))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    end_time = time.time()
    duration = end_time - start_time
    print(f"\n[{num_clients} client(s)] Temps: {duration:.2f}s")
    return duration

if __name__ == "__main__":
    results = []
    for clients in [1, 2, 3]:
        duration = run_scaling_test(clients)
        results.append((clients, duration))

    print("\n Resultats Multi-node (Filter):")
    base = results[0][1]
    for c, d in results:
        print(f"{c} clients ➝ {d:.2f}s")
        if c > 1:
            speedup = base / d
            print(f" Speedup amb {c} clients: {speedup:.2f}x")

    data = []
    base_time = results[0][1]

    for clients, duration in results:
        speedup = base_time / duration if clients > 1 else 1.0
        data.append({
            "Test": "InsultFilter",
            "Middleware": "PyRO",
            "Mode": "Multi-node",
            "Clients": clients,
            "Num Tasks": NUM_TEXTS,
            "Temps Total (s)": round(duration, 2),
            "Speedup": round(speedup, 2)
        })

    guardar_resultats(data, sheet_name="PyRO_Multi_Filter")