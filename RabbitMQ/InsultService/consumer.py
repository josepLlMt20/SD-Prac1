import pika
from RabbitMQ.insults_data import add_insult
from RabbitMQ.constants import INSULT_QUEUE

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue=INSULT_QUEUE)

print("InsultConsumer waiting for insults...")

def callback(ch, method, properties, body):
    insult = body.decode()
    if add_insult(insult):
        print(f"Stored insult: {insult}")
    else:
        print(f"Duplicate insult ignored: {insult}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=INSULT_QUEUE, on_message_callback=callback)
channel.start_consuming()
