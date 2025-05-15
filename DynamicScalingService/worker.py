import pika
import time
import re
import sys

INSULTS = ["idiot", "stupid", "dumb", "fool"]

def censor_text(text):
    pattern = re.compile(r'\b(' + '|'.join(re.escape(word) for word in INSULTS) + r')\b', re.IGNORECASE)
    return pattern.sub("CENSORED", text)

def callback_factory(worker_id):
    def callback(ch, method, properties, body):
        original = body.decode()
        censored = censor_text(original)
        print(f"[{worker_id}] Original: {original}")
        print(f"[{worker_id}] Censored: {censored}\n")
        time.sleep(0.5)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    return callback

def start_worker(worker_id="Worker"):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='insult_queue')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='insult_queue', on_message_callback=callback_factory(worker_id))
    print(f"[{worker_id}] Started and waiting for messages.")
    channel.start_consuming()

if __name__ == "__main__":
    worker_id = sys.argv[1] if len(sys.argv) > 1 else "Worker"
    start_worker(worker_id)
