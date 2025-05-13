import pika
import threading
import time

# Parámetros
NUM_INSULTS   = 1000
INSULT_QUEUE  = "insult_queue"
NUM_NODES     = [1, 2, 3]

def service_node(node_id, stop_event):
    local_set = set()
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    ch   = conn.channel()
    ch.queue_declare(queue=INSULT_QUEUE)

    def callback(ch, method, props, body):
        insult = body.decode()
        if insult not in local_set:
            local_set.add(insult)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    ch.basic_qos(prefetch_count=1)
    ch.basic_consume(queue=INSULT_QUEUE, on_message_callback=callback)

    print(f"[Node-{node_id}] On, esperant insults…")
    while not stop_event.is_set():
        ch._process_data_events(time_limit=1)
    conn.close()
    print(f"[Node-{node_id}] Aturat. Total: {len(local_set)}")

def run_scaling_test(num_nodes):
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    ch   = conn.channel()
    ch.queue_declare(queue=INSULT_QUEUE)
    ch.queue_purge(queue=INSULT_QUEUE)
    conn.close()

    stop_events = []
    threads = []
    for nid in range(1, num_nodes + 1):
        ev = threading.Event()
        t  = threading.Thread(target=service_node, args=(nid, ev), daemon=True)
        t.start()
        stop_events.append(ev)
        threads.append(t)

    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    ch   = conn.channel()
    print(f"\n[TEST] Publicant {NUM_INSULTS} insults amb {num_nodes} node(s)…")
    start = time.time()
    for i in range(NUM_INSULTS):
        ch.basic_publish(exchange='', routing_key=INSULT_QUEUE, body=f"Insult-{i}")

    while True:
        q = ch.queue_declare(queue=INSULT_QUEUE, passive=True)
        if q.method.message_count == 0:
            break
        time.sleep(0.05)
    end = time.time()
    duration = end - start

    for ev in stop_events:
        ev.set()
    for t in threads:
        t.join()

    conn.close()
    print(f"[RESULT] Node(s)={num_nodes} → Temps total (pub+proc): {duration:.2f}s")
    return duration

if __name__ == "__main__":
    results = []
    for n in NUM_NODES:
        dur = run_scaling_test(n)
        results.append((n, dur))

    print("\n📊 Speedup:")
    base = results[0][1]
    for nodes, dur in results:
        speedup = base / dur
        print(f" • {nodes} node(s): {dur:.2f}s → {speedup:.2f}×")
