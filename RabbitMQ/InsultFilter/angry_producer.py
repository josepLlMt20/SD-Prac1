import pika
import time
import random

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue='text_queue')

angry_lines = [
    "Eres más inútil que un cenicero en una moto.",
    "Tu código es como el horóscopo: pura ficción.",
    "Eres más lento que un caracol cojo.",
    "Tu lógica es tan clara como un café con leche.",
    "Eres más pesado que un lunes por la mañana.",
    "Tu código es tan limpio como un basurero.",
    "Eres más torpe que un pez en una bicicleta.",
    "Tu sentido del humor es más plano que una hoja de papel.",
    "Eres más aburrido que ver crecer la hierba.",
]

while True:
    text = f"Insult: {random.choice(angry_lines)}"
    channel.basic_publish(exchange='', routing_key='text_queue', body=text)
    print(f"[AngryProducer] Enviat: {text}")
    time.sleep(3)
