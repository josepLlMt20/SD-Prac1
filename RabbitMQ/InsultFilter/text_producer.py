import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue='text_queue')

# Envia missatges sense insults a la text_queue
i = 0
while True:
    text = f"Missatge sense insults {i}."
    channel.basic_publish(exchange='', routing_key='text_queue', body=text)
    print(f"[TextProducer] Enviat: {text}")
    i += 1
    time.sleep(5)
