import xmlrpc.client
import threading
import time
from StressTests.data_manager import guardar_resultats

NUM_REQUESTS = 300

def add_insults(thread_id, start_idx, end_idx):
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
    for i in range(start_idx, end_idx):
        proxy.add_insult(f"insult-{thread_id}-{i}")

def run_scaling_test(num_clients):
    print(f"\n Test amb {num_clients} client(s)...")
    insults_per_client = NUM_REQUESTS // num_clients
    threads = []
    start_time = time.time()

    for i in range(num_clients):
        t = threading.Thread(
            target=add_insults,
            args=(i + 1, i * insults_per_client, (i + 1) * insults_per_client)
        )
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    end_time = time.time()
    duration = end_time - start_time
    print(f"⏱ Temps total: {duration:.2f}s")
    return duration

if __name__ == "__main__":
    results = []
    for clients in [1, 2, 3]:
        duration = run_scaling_test(clients)
        results.append((clients, duration))

    print("\n Resultats finals:")
    for clients, dur in results:
        print(f"{clients} clients ➝ {dur:.2f}s")

    baseline = results[0][1]
    for clients, dur in results[1:]:
        speedup = baseline / dur
        print(f" Speedup amb {clients} clients: {speedup:.2f}x")
