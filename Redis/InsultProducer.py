import redis
import time
import random

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

queue_name = "insult_queue"
insults = [
    "Eres más lento que una tortuga en arena movediza.",
    "Tienes menos carisma que un ladrillo mojado.",
    "Pareces un error 404: personalidad no encontrada."
]

while True:
    insult = random.choice(insults)
    client.rpush(queue_name, insult)  # Agrega el insulto a la cola
    print(f"Produced: {insult}")
    time.sleep(5)
