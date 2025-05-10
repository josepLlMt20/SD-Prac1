import pika
import time

# Conectar a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='insult_exchange', exchange_type='fanout')

stored_insults = [
    "Eres más inútil que un tenedor en sopa.",
    "Tienes menos carisma que un ladrillo mojado."
]

# Publica insults cada 5s a l'exchange
while True:
    for insult in stored_insults:
        channel.basic_publish(exchange='insult_exchange', routing_key='', body=insult)
        print(f"INSULT ENVIAT A RECIEVER: {insult}")
    time.sleep(5)