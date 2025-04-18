import pika
import time
from RabbitMQ.insults_data import get_insults
from RabbitMQ.constants import INSULT_CHANNEL

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.exchange_declare(exchange=INSULT_CHANNEL, exchange_type='fanout')

print("InsultBroadcaster started.")
while True:
    insults = get_insults()
    if insults:
        insult = insults[0]
        channel.basic_publish(exchange=INSULT_CHANNEL, routing_key='', body=insult)
        print(f"Broadcasted insult: {insult}")
    time.sleep(5)