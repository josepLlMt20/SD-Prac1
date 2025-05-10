import pika
import time

from main import print_hi

NUM_INSULTS = 300
INSULT_QUEUE = "insult_queue"

print(f"[STRESS TEST RABBITMQ] Enviant {NUM_INSULTS} insults a la cua '{INSULT_QUEUE}'...")

# Conexió a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue=INSULT_QUEUE)

start_time = time.time()

# Generarem tants insults com NUM_INSULTS (300) i els publicarem a la cua
for i in range(NUM_INSULTS):
    insult = f"Generated insult #{i}"
    channel.basic_publish(exchange='', routing_key=INSULT_QUEUE, body=insult.encode())
    print(f"Text enviat: {insult}")

connection.close()

end_time = time.time()
duration = end_time - start_time
rps = NUM_INSULTS / duration

print(f"\n📊 Resultats RabbitMQ (Single-node):")
print(f" - Temps total: {duration:.2f}s")
print(f" - RPS (requests/second): {rps:.2f}")