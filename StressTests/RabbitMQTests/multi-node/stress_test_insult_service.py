import pika
import time
import threading

NUM_INSULTS = 300
INSULT_QUEUE = "insult_queue"

# Funció de representa un client enviant insults
def send_insults(client_id, num_insults_per_client):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=INSULT_QUEUE)   # Declarem la cua d'insults

    for i in range(num_insults_per_client):
        insult = f"Insult-{client_id}-{i}"
        channel.basic_publish(exchange='', routing_key=INSULT_QUEUE, body=insult.encode())
    connection.close()

def run_scaling_test(num_clients):
    insults_per_client = NUM_INSULTS // num_clients # Dividim els insults entre els clients
    threads = []
    start_time = time.time()

    # Per cada client cridarem send_insults()
    for i in range(num_clients):
        #start = i * insults_per_client
        #end = (i + 1) * insults_per_client
        #t = threading.Thread(target=send_insults, args=(i + 1, start, end))
        t = threading.Thread(target=send_insults, args=(i + 1, insults_per_client))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    end_time = time.time()
    duration = end_time - start_time
    print(f"\n[{num_clients} client(s)] Temps: {duration:.2f}s")
    return duration

if __name__ == "__main__":
    print(" Reiniciant cua d'insults...")
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=INSULT_QUEUE)
    channel.queue_purge(queue=INSULT_QUEUE)
    connection.close()

    resultados = []
    for clients in [1, 2, 3]:
        duration = run_scaling_test(clients)
        resultados.append((clients, duration))

    print("\n Resultats Multi-node (Insult Producer):")
    base = resultados[0][1]
    for c, d in resultados:
        print(f"{c} clients ➝ {d:.2f}s")
        if c > 1:       # 1 client no té speedup per comprovar
            speedup = base / d
            print(f" Speedup amb {c} clients: {speedup:.2f}x")