import pika
import threading
import time
import random
import re
from StressTests.data_manager import guardar_resultats
from datetime import datetime

NUM_TEXTS     = 1000
NUM_WORKERS   = 1
INSULT_QUEUE  = "insult_queue"
TEXT_QUEUE    = "text_queue"
RESULT_QUEUE  = "results_queue"

INSULTS  = ["inútil", "cenicero", "ficción", "caracol", "cojo"]
SUBJECTS = ["Mi jefe", "El conductor", "Mi vecino", "Ese tipo", "El cliente"]
ACTIONS  = ["es un", "parece un", "se comporta como un", "claramente es un"]

conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
ch   = conn.channel()
for q in (INSULT_QUEUE, TEXT_QUEUE, RESULT_QUEUE):
    ch.queue_declare(queue=q)
    ch.queue_purge(queue=q)
print("[INIT] Reset de les cues.")

for insult in INSULTS:
    ch.basic_publish(exchange='', routing_key=INSULT_QUEUE, body=insult)
print(f"[INIT] Publicats {len(INSULTS)} insults a '{INSULT_QUEUE}'.")
insult_set = set(INSULTS)

def worker_fn(id):
    wconn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    wch   = wconn.channel()
    wch.queue_declare(queue=TEXT_QUEUE)
    wch.queue_declare(queue=RESULT_QUEUE)
    print(f"[Worker-{id}] Engegat.")

    def on_message(ch, method, props, body):
        text = body.decode()
        filtered = text
        for insult in insult_set:
            filtered = re.sub(rf'\b{re.escape(insult)}\b', "CENSORED", filtered, flags=re.IGNORECASE)
        ch.basic_publish(exchange='', routing_key=RESULT_QUEUE, body=filtered)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    wch.basic_qos(prefetch_count=1)
    wch.basic_consume(queue=TEXT_QUEUE, on_message_callback=on_message)
    wch.start_consuming()

for i in range(NUM_WORKERS):
    t = threading.Thread(target=worker_fn, args=(i+1,), daemon=True)
    t.start()

print(f"[STRESS TEST] Enviant i processant {NUM_TEXTS} textos amb {NUM_WORKERS} worker(s)…")
start = time.time()

for i in range(NUM_TEXTS):
    subj   = random.choice(SUBJECTS)
    act    = random.choice(ACTIONS)
    insult = random.choice(INSULTS)
    text   = f"{subj} {act} {insult}."
    ch.basic_publish(exchange='', routing_key=TEXT_QUEUE, body=text)
    if (i+1) % 100 == 0:
        print(f"  → Enviats {i+1}/{NUM_TEXTS}")

while True:
    q = ch.queue_declare(queue=RESULT_QUEUE, passive=True)
    processed = q.method.message_count
    if processed >= NUM_TEXTS:
        break
    print(f"    ➤ Processats {processed}/{NUM_TEXTS}…")
    time.sleep(0.5)

end = time.time()
total = end - start
rps   = NUM_TEXTS / total

print("\n📊 RESULTATS:")
print(f" - Temps total (enviament + processat): {total:.2f} s")
print(f" - Throughput: {rps:.2f} msg/s")

# ✅ Guardar en Excel
result = {
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "num_texts": NUM_TEXTS,
    "num_workers": NUM_WORKERS,
    "total_time_sec": round(total, 2),
    "throughput_msgs_per_sec": round(rps, 2)
}
guardar_resultats([result], sheet_name="InsultFilterTest")

conn.close()
