import pika
import time
from RabbitMQ.constants import TEXT_QUEUE

# Genera texts amb normals cada 5 segons

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue=TEXT_QUEUE)

i = 0
while True:
    text = f"This is a clean text message number {i}."
    channel.basic_publish(exchange='', routing_key=TEXT_QUEUE, body=text)
    print(f"Produced clean text: {text}")
    i += 1
    time.sleep(5)