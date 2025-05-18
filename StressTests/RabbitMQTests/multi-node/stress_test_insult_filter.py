import pika
import threading
import time
import random
import re
from StressTests.data_manager import guardar_resultats
from datetime import datetime

TASK_SIZES = [1000, 2500, 5000, 10000]
WORKERS_LIST = [1, 2, 3]
INSULT_QUEUE = "insult_queue"
TEXT_QUEUE = "text_queue"
RESULT_QUEUE = "results_queue"

INSULTS = ["inútil", "cenicero", "pichon", "caracol", "cojo"]
INSULTS_SET = set(INSULTS)
SUBJECTS = ["Mi jefe", "El conductor", "Mi vecino", "Ese tipo", "El cliente"]
ACTIONS = ["es un", "parece un", "se comporta como un", "claramente es un"]

def worker_fn(worker_id, stop_event):
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    ch = conn.channel()
    ch.queue_declare(queue=TEXT_QUEUE)
    ch.queue_declare(queue=RESULT_QUEUE)
    ch.basic_qos(prefetch_count=1)

    def on_text(ch, method, props, body):
        text = body.decode()
        filtered = text
        for insult in INSULTS_SET:
            filtered = re.sub(rf'\b{re.escape(insult)}\b', "CENSORED", filtered, flags=re.IGNORECASE)
        ch.basic_publish(exchange='', routing_key=RESULT_QUEUE, body=filtered)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    ch.basic_consume(queue=TEXT_QUEUE, on_message_callback=on_text)
    while not stop_event.is_set():
        ch._process_data_events(time_limit=1)
    conn.close()

def run_scaling_test(num_workers, num_msgs):
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    ch = conn.channel()
    for q in (INSULT_QUEUE, TEXT_QUEUE, RESULT_QUEUE):
        ch.queue_declare(queue=q)
        ch.queue_purge(queue=q)

    for insult in INSULTS:
        ch.basic_publish(exchange='', routing_key=INSULT_QUEUE, body=insult)

    stop_events = []
    for i in range(num_workers):
        ev = threading.Event()
        t = threading.Thread(target=worker_fn, args=(i + 1, ev), daemon=True)
        t.start()
        stop_events.append(ev)

    start = time.time()
    for i in range(num_msgs):
        subj = random.choice(SUBJECTS)
        act = random.choice(ACTIONS)
        insult = random.choice(INSULTS)
        text = f"{subj} {act} {insult}."
        ch.basic_publish(exchange='', routing_key=TEXT_QUEUE, body=text)

    while True:
        q = ch.queue_declare(queue=RESULT_QUEUE, passive=True)
        if q.method.message_count >= num_msgs:
            break
        time.sleep(0.1)
    end = time.time()

    for ev in stop_events:
        ev.set()

    conn.close()
    return end - start

if __name__ == "__main__":
    all_results = []

    for num_msgs in TASK_SIZES:
        results = []
        for w in WORKERS_LIST:
            dur = run_scaling_test(w, num_msgs)
            results.append((w, dur))

        base_time = results[0][1]
        for w, dur in results:
            speedup = base_time / dur if w > 1 else 1.0
            print(f" • Workers={w}, Msgs={num_msgs} → {dur:.2f}s (speedup: {speedup:.2f}x)")
            all_results.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Test": "InsultFilter",
                "Middleware": "RabbitMQ",
                "Mode": "Multi-node",
                "Clients": w,
                "Num Tasks": num_msgs,
                "Temps Total (s)": round(dur, 2),
                "Speedup": round(speedup, 2)
            })

    guardar_resultats(all_results, sheet_name="RabbitMQ_Multi_Filter")
