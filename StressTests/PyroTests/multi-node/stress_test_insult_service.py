import Pyro4
import time
import threading

NUM_INSULTS = 300

def add_insults(client_id, num_insults_per_client):
    insult_service = Pyro4.Proxy("PYRONAME:InsultService")
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
    resultados = []
    for clients in [1, 2, 3]:
        duracion = run_scaling_test(clients)
        resultados.append((clients, duracion))

    print("\n Resultats Multi-node (Insult Adder):")
    base = resultados[0][1]
    for c, d in resultados:
        print(f"{c} clients ➝ {d:.2f}s")
        if c > 1:
            speedup = base / d
            print(f" Speedup amb {c} clients: {speedup:.2f}x")