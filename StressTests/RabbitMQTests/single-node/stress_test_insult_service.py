import pika
import time

NUM_INSULTS  = 1_000
INSULT_QUEUE = "insult_queue"

print(f"[STRESS TEST RabbitMQ] Publicando {NUM_INSULTS} insults…")

conn    = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = conn.channel()
channel.queue_declare(queue=INSULT_QUEUE)
channel.queue_purge(queue=INSULT_QUEUE)

start = time.time()
for i in range(NUM_INSULTS):
    payload = f"Generated insult #{i}"
    channel.basic_publish(exchange='', routing_key=INSULT_QUEUE, body=payload)
end = time.time()

duration = end - start
rps      = NUM_INSULTS / duration
print(f"\n📊 Resultados Producer (Single-node):")
print(f" • Tiempo envío: {duration:.3f}s")
print(f" • Throughput:  {rps:.0f} msg/s")

channel.close()
conn.close()
