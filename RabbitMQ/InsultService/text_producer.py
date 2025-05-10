import pika
import time
import random

# Conexió a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declarar la cua
channel.queue_declare(queue='insult_queue')

insults = [
    "Eres más inútil que un cenicero en una moto.",
    "Tienes menos neuronas que un ladrillo.",
    "Eres más lento que un caracol cojo."
]

# Produeix insults i els envia a la insult_queue
while True:
    insult = random.choice(insults)
    channel.basic_publish(exchange='', routing_key='insult_queue', body=insult)
    print(f"Enviat: {insult}")
    time.sleep(5)