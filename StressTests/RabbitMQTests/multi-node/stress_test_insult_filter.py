import pika
import time
import threading
import random

NUM_TEXTS = 300
TEXT_QUEUE = "text_queue"
INSULTS = ["inútil", "cenicero", "ficción", "caracol", "cojo"]
SUBJECTS = ["Mi jefe", "El conductor", "Mi vecino", "Ese tipo", "El cliente"]
ACTIONS = ["es un", "parece un", "se comporta como un", "claramente es un"]

def send_texts(client_id, num_texts_per_client):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=TEXT_QUEUE)
    for i in range(num_texts_per_client):
        subject = random.choice(SUBJECTS)
        action = random.choice(ACTIONS)
        insult = random.choice(INSULTS)
        text = f"{subject} {action} {insult} (Client {client_id}-{i})."
        channel.basic_publish(exchange='', routing_key=TEXT_QUEUE, body=text.encode())
        print(f"[TextProducer {client_id}] Enviat: {text}")
    connection.close()

def run_scaling_test(num_clients):
    texts_per_client = NUM_TEXTS // num_clients
    threads = []
    start_time = time.time()

    for i in range(num_clients):
        t = threading.Thread(target=send_texts, args=(i + 1, texts_per_client))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    end_time = time.time()
    duration = end_time - start_time
    print(f"\n[{num_clients} client(s)] Temps: {duration:.2f}s")
    return duration

if __name__ == "__main__":
    print(" Reiniciant cua de textos per filtrar...")
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=TEXT_QUEUE)
    channel.queue_purge(queue=TEXT_QUEUE)
    connection.close()

    resultados = []
    for clients in [1, 2, 3]:
        duration = run_scaling_test(clients)
        resultados.append((clients, duration))

    print("\n Resultats Multi-node (Filter Text Producer):")
    base = resultados[0][1]
    for c, d in resultados:
        print(f"{c} clients ➝ {d:.2f}s")
        if c > 1:
            speedup = base / d
            print(f" Speedup amb {c} clients: {speedup:.2f}x")