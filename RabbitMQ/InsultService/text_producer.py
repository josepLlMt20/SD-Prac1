import pika
import time
from RabbitMQ.constants import INSULT_QUEUE

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue=INSULT_QUEUE)

insults = [
    "You're as useless as the 'ueue' in 'queue'.",
    "You bring everyone joy… when you leave the room.",
    "You're the reason the gene pool needs a lifeguard."
]

i = 0
while True:
    insult = insults[i % len(insults)]
    channel.basic_publish(exchange='', routing_key=INSULT_QUEUE, body=insult)
    print(f"Produced insult: {insult}")
    i += 1
    time.sleep(5)