import pika

# Lista en memoria para evitar duplicados
stored_insults = set()

# Conectar a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='insult_queue')


def callback(ch, method, properties, body):
    insult = body.decode()

    if insult not in stored_insults:  # Evita duplicados
        stored_insults.add(insult)
        print(f"Stored: {insult}")


channel.basic_consume(queue='insult_queue', on_message_callback=callback, auto_ack=True)

print("Waiting for insults...")
channel.start_consuming()