import pika

# Llista en memoria per evitar duplicats
stored_insults = set()

# Conectar a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='insult_queue')

# Consumeix insults
def callback(ch, method, properties, body):
    insult = body.decode()

    if insult not in stored_insults:  # Evita duplicats
        stored_insults.add(insult)
        print(f"Guardat: {insult}")


channel.basic_consume(queue='insult_queue', on_message_callback=callback, auto_ack=True)

print("Esperant Insults...")
channel.start_consuming()