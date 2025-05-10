import pika
import time
import random

NUM_TEXTS = 300
TEXT_QUEUE = "text_queue"
INSULTS = ["inútil", "cenicero", "ficción", "caracol", "cojo"]
SUBJECTS = ["Mi jefe", "El conductor", "Mi vecino", "Ese tipo", "El cliente"]
ACTIONS = ["es un", "parece un", "se comporta como un", "claramente es un"]

print(f"[STRESS TEST RABBITMQ FILTER TEXT PRODUCER] Enviant {NUM_TEXTS} textos a la cua '{TEXT_QUEUE}'...")

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue=TEXT_QUEUE)     # Declarem la cua de textos

start_time = time.time()

for i in range(NUM_TEXTS):
    subject = random.choice(SUBJECTS)
    action = random.choice(ACTIONS)
    insult = random.choice(INSULTS)
    text = f"{subject} {action} {insult}."
    channel.basic_publish(exchange='', routing_key=TEXT_QUEUE, body=text.encode())
    print(f"[TextProducer] Enviat: {text}")

end_time = time.time()
duration = end_time - start_time
rps = NUM_TEXTS / duration

print(f"\n📊 Resultats RabbitMQ Filter Text Producer (Single-node):")
print(f" - Temps total: {duration:.2f}s")
print(f" - RPS (requests/second): {rps:.2f}")
connection.close()