import pika
import time
from StressTests.data_manager import guardar_resultats
from datetime import datetime

NUM_INSULTS  = 1000
INSULT_QUEUE = "insult_queue"

print(f"[STRESS TEST RabbitMQ] Publicant {NUM_INSULTS} insults…")

conn    = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = conn.channel()
channel.queue_declare(queue=INSULT_QUEUE)
channel.queue_purge(queue=INSULT_QUEUE)

start = time.time()
for i in range(NUM_INSULTS):
    payload = f"INSULT #{i}"
    channel.basic_publish(exchange='', routing_key=INSULT_QUEUE, body=payload)
end = time.time()

duration = end - start
rps      = NUM_INSULTS / duration
print(f"\n📊 RESULTATS (Single-node):")
print(f" • Temps enviament: {duration:.3f}s")
print(f" • Throughput:  {rps:.0f} msg/s")

# ✅ Guardar en Excel
result = {
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "num_insults": NUM_INSULTS,
    "total_time_sec": round(duration, 2),
    "throughput_msgs_per_sec": round(rps, 2)
}
guardar_resultats([result], sheet_name="InsultServiceTest")

channel.close()
conn.close()
