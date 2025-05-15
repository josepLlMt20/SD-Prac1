import Pyro4
import time
import threading
from StressTests.data_manager import guardar_resultats

NUM_INSULTS = 1000

def add_insults(client_id, num_insults_per_client):
    insult_service = Pyro4.Proxy("PYRONAME:InsultService1")
    for i in range(num_insults_per_client):
        insult = f"Client-{client_id}-Insult-{i}"
        insult_service.add_insult(insult)
        print(f"Text Afegit: {insult}")

def run_scaling_test(num_clients):
    insults_per_client = NUM_INSULTS // num_clients
    threads = []
    start_time = time.time()

    for i in range(num_clients):
        t = threading.Thread(target=add_insults, args=(i + 1, insults_per_client))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    end_time = time.time()
    duration = end_time - start_time
    print(f"\n[{num_clients} client(s)] Temps: {duration:.2f}s")
    return duration

if __name__ == "__main__":
    resultats = []
    for clients in [1, 2, 3]:
        duracio = run_scaling_test(clients)
        resultats.append((clients, duracio))

    print("\n Resultats Multi-node (Insult Adder):")
    base = resultats[0][1]
    for c, d in resultats:
        print(f"{c} clients ➝ {d:.2f}s")
        if c > 1:
            speedup = base / d
            print(f" Speedup amb {c} clients: {speedup:.2f}x")

    data = []
    base_time = resultats[0][1]

    for clients, duration in resultats:
        speedup = base_time / duration if clients > 1 else 1.0
        data.append({
            "Test": "InsultService1",
            "Middleware": "PyRO",
            "Mode": "Multi-node",
            "Clients": clients,
            "Num Tasks": NUM_INSULTS,
            "Temps Total (s)": round(duration, 2),
            "Speedup": round(speedup, 2)
        })

    guardar_resultats(data, sheet_name="PyRO_Multi_Service")