import pika
from RabbitMQ.constants import TEXT_QUEUE, RESULT_LIST_FILE
from RabbitMQ.insults_data import get_insults

# Encarregat de filtrar els insults dels texts

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue=TEXT_QUEUE)
channel.queue_declare(queue='filtered_results')

print("InsultFilter worker started.")

def callback(ch, method, properties, body):
    text = body.decode()
    insults = get_insults()
    filtered = text
    for insult in insults:
        filtered = filtered.replace(insult, "CENSORED")
    with open(RESULT_LIST_FILE, "a") as f:
        f.write(filtered + "\n")
    print(f"Filtered: {filtered}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=TEXT_QUEUE, on_message_callback=callback)
channel.start_consuming()