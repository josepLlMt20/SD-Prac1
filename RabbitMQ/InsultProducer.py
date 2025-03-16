import pika
import time
import random

# Conexión a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declarar la cola
channel.queue_declare(queue='insult_queue')

insults = [
    "Eres más inútil que un cenicero en una moto.",
    "Tienes menos neuronas que un ladrillo.",
    "Eres más lento que un caracol cojo."
]

while True:
    insult = random.choice(insults)
    channel.basic_publish(exchange='', routing_key='insult_queue', body=insult)
    print(f"Produced: {insult}")
    time.sleep(5)
