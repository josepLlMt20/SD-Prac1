import pika
import re
import threading

insults = set()

def start_insult_listener():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue='insult_queue')

    def insult_callback(ch, method, properties, body):
        insult = body.decode().strip()
        insults.add(insult.lower())
        print(f"[+] New insult added to memory: {insult}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='insult_queue', on_message_callback=insult_callback)
    print("[→] Listening for new insults...")
    channel.start_consuming()

def start_text_listener():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue='text_queue')
    result_channel = connection.channel()
    result_channel.queue_declare(queue='results_queue')

    def text_callback(ch, method, properties, body):
        text = body.decode()
        filtered = text
        for insult in insults:
            pattern = re.compile(re.escape(insult), re.IGNORECASE)
            filtered = pattern.sub("CENSORED", filtered)
        result_channel.basic_publish(exchange='', routing_key='results_queue', body=filtered)
        print(f"[✔] Filtered text: {filtered}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='text_queue', on_message_callback=text_callback)
    print("[→] Listening for texts to filter...")
    channel.start_consuming()

threading.Thread(target=start_insult_listener, daemon=True).start()
start_text_listener()
