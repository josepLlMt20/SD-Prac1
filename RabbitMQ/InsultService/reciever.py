import pika
from RabbitMQ.constants import INSULT_CHANNEL

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.exchange_declare(exchange=INSULT_CHANNEL, exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange=INSULT_CHANNEL, queue=queue_name)

print("InsultReceiver listening for messages...")

def callback(ch, method, properties, body):
    print(f"Received insult: {body.decode()}")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()