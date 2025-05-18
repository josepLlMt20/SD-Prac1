import pika
import threading
import time
from StressTests.data_manager import guardar_resultats
from datetime import datetime

TASK_SIZES = [1000, 2500, 5000, 10000]
NUM_NODES = [1, 2, 3]
INSULT_QUEUE = "insult_queue"

def service_node(node_id, stop_event):
    local_set = set()
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    ch = conn.channel()
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

def run_scaling_test(num_nodes, num_msgs):
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    ch = conn.channel()
    ch.queue_declare(queue=INSULT_QUEUE)
    ch.queue_purge(queue=INSULT_QUEUE)
    conn.close()

    stop_events, threads = [], []
    for nid in range(1, num_nodes + 1):
        ev = threading.Event()
        t = threading.Thread(target=service_node, args=(nid, ev), daemon=True)
        t.start()
        stop_events.append(ev)
        threads.append(t)

    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    ch = conn.channel()
    print(f"\n[TEST] Publicant {num_msgs} insults amb {num_nodes} node(s)…")
    start = time.time()
    for i in range(num_msgs):
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
    return duration

if __name__ == "__main__":
    all_results = []

    for num_msgs in TASK_SIZES:
        results = []
        for n in NUM_NODES:
            dur = run_scaling_test(n, num_msgs)
            results.append((n, dur))

        base_time = results[0][1]
        for n, dur in results:
            speedup = base_time / dur if n > 1 else 1.0
            print(f" • Nodes={n}, Msgs={num_msgs} → {dur:.2f}s (speedup: {speedup:.2f}x)")
            all_results.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Test": "InsultService",
                "Middleware": "RabbitMQ",
                "Mode": "Multi-node",
                "Clients": n,
                "Num Tasks": num_msgs,
                "Temps Total (s)": round(dur, 2),
                "Speedup": round(speedup, 2)
            })

    guardar_resultats(all_results, sheet_name="RabbitMQ_Multi_Service")
