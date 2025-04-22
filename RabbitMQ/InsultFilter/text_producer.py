import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue='text_queue')

i = 0
while True:
    text = f"This is a clean text message number {i}."
    channel.basic_publish(exchange='', routing_key='text_queue', body=text)
    print(f"[TextProducer] Sent: {text}")
    i += 1
    time.sleep(5)
