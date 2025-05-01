import redis
import time
import threading

NUM_INSULTS = 300
INSULT_QUEUE = "insult_queue"

def send_insults(client_id, start, end):
    r = redis.Redis(decode_responses=True)
    for i in range(start, end):
        insult = f"Insulto-{client_id}-{i}"
        r.rpush(INSULT_QUEUE, insult)

def run_scaling_test(num_clients):
    insults_per_client = NUM_INSULTS // num_clients
    threads = []
    start_time = time.time()

    for i in range(num_clients):
        start = i * insults_per_client
        end = (i + 1) * insults_per_client
        t = threading.Thread(target=send_insults, args=(i + 1, start, end))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    end_time = time.time()
    duration = end_time - start_time
    print(f"\n[{num_clients} client(s)] Temps: {duration:.2f}s")
    return duration

if __name__ == "__main__":
    print(" Reiniciant insult_queue...")
    r = redis.Redis(decode_responses=True)
    r.delete(INSULT_QUEUE)

    resultados = []
    for clients in [1, 2, 3]:
        duracion = run_scaling_test(clients)
        resultados.append((clients, duracion))

    print("\n Resultats:")
    for c, d in resultados:
        print(f"{c} clients ➝ {d:.2f}s")

    base = resultados[0][1]
    for c, d in resultados[1:]:
        print(f" Speedup amb {c} clients: {base/d:.2f}x")
