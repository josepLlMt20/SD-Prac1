import pika
import time
import random

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='insult_queue')

insults = ["idiot", "stupid", "fool", "dumb"]
phrases = [
    "You are such an {}!",
    "Only a {} would say that.",
    "Hey {}, that's not cool.",
    "This message is clean and polite.",
    "Have a great day!",
    "Let's go for a walk.",
    "What a {} thing to do!",
    "No insults here, just kindness."
]

try:
    while True:
        if random.random() < 0.5:
            insult = random.choice(insults)
            phrase = random.choice([p for p in phrases if "{}" in p]).format(insult)
        else:
            phrase = random.choice([p for p in phrases if "{}" not in p])

        channel.basic_publish(exchange='', routing_key='insult_queue', body=phrase)
        print(f" [→] Sent: {phrase}")
        time.sleep(0.05)
except KeyboardInterrupt:
    print("Producer stopped")
    connection.close()
