import pika

# Conectar a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Vincular al exchange
# Escolta insults publicats per l'exchange
channel.exchange_declare(exchange='insult_exchange', exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='insult_exchange', queue=queue_name)

def callback(ch, method, properties, body):
    print(f"Rebut: {body.decode()}")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print("Esperant Insults...")
channel.start_consuming()