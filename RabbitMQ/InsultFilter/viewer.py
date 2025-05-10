import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue='results_queue')

# Consumeix i mostra els missatges de la cua de resultats de filter.py
print("Resultats filtrats:")

def callback(ch, method, properties, body):
    print(f"- {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='results_queue', on_message_callback=callback)
channel.start_consuming()
