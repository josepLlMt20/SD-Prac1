import pika
import threading
import time
import random
import re

# Parámetros
NUM_TEXTS    = 1000
INSULT_QUEUE = "insult_queue"
TEXT_QUEUE   = "text_queue"
RESULT_QUEUE = "results_queue"
WORKERS      = [1, 2, 3]

INSULTS  = ["inútil", "cenicero", "pichon", "caracol", "cojo"]
INSULTS_SET = set(INSULTS)

SUBJECTS = ["Mi jefe", "El conductor", "Mi vecino", "Ese tipo", "El cliente"]
ACTIONS  = ["es un", "parece un", "se comporta como un", "claramente es un"]

def worker_fn(worker_id, stop_event):
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    ch   = conn.channel()
    ch.queue_declare(queue=TEXT_QUEUE)
    ch.queue_declare(queue=RESULT_QUEUE)
    ch.basic_qos(prefetch_count=1)
    print(f"[Worker-{worker_id}] Engegat.")

    def on_text(ch, method, props, body):
        text = body.decode()
        filtered = text
        for insult in INSULTS_SET:
            filtered = re.sub(rf'\b{re.escape(insult)}\b',
                              "CENSORED",
                              filtered,
                              flags=re.IGNORECASE)
        ch.basic_publish(exchange='', routing_key=RESULT_QUEUE, body=filtered)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    ch.basic_consume(queue=TEXT_QUEUE, on_message_callback=on_text)

    while not stop_event.is_set():
        ch._process_data_events(time_limit=1)
    conn.close()
    print(f"[Worker-{worker_id}] Aturat.")

def run_scaling_test(num_workers):
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    ch   = conn.channel()
    for q in (INSULT_QUEUE, TEXT_QUEUE, RESULT_QUEUE):
        ch.queue_declare(queue=q)
        ch.queue_purge(queue=q)

    for insult in INSULTS:
        ch.basic_publish(exchange='', routing_key=INSULT_QUEUE, body=insult)
    print(f"\n[INIT] {len(INSULTS)} insults precarregats a '{INSULT_QUEUE}'")

    stop_events = []
    for i in range(num_workers):
        ev = threading.Event()
        t  = threading.Thread(target=worker_fn, args=(i+1, ev), daemon=True)
        t.start()
        stop_events.append(ev)

    print(f"[STRESS TEST] Encuant {NUM_TEXTS} textos a '{TEXT_QUEUE}'…")
    start = time.time()
    for i in range(NUM_TEXTS):
        subj   = random.choice(SUBJECTS)
        act    = random.choice(ACTIONS)
        insult = random.choice(INSULTS)
        text   = f"{subj} {act} {insult}."
        ch.basic_publish(exchange='', routing_key=TEXT_QUEUE, body=text)

    while True:
        q = ch.queue_declare(queue=RESULT_QUEUE, passive=True)
        if q.method.message_count >= NUM_TEXTS:
            break
        time.sleep(0.1)
    end = time.time()

    for ev in stop_events:
        ev.set()

    duration = end - start
    print(f"[RESULT] {num_workers} worker(s) → Temps total: {duration:.2f}s")
    conn.close()
    return duration

if __name__ == "__main__":
    results = []
    for w in WORKERS:
        dur = run_scaling_test(w)
        results.append((w, dur))

    print("\n📊 Speedups:")
    base = results[0][1]
    for w, dur in results:
        speedup = base / dur
        print(f" • {w} worker(s): {dur:.2f}s → {speedup:.2f}×")
