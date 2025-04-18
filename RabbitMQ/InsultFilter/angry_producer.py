import pika
import time
from RabbitMQ.constants import TEXT_QUEUE

# Genera texts amb insults cada 5 segons

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue=TEXT_QUEUE)

insults = [
    "You're as useless as the 'ueue' in 'queue'.",
    "You bring everyone joy… when you leave the room."
]

i = 0
while True:
    text = f"Here's an angry message: {insults[i % len(insults)]}"
    channel.basic_publish(exchange='', routing_key=TEXT_QUEUE, body=text)
    print(f"Produced angry text: {text}")
    i += 1
    time.sleep(5)