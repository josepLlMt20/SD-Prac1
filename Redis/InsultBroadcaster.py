import redis
import time

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

insult_list = "INSULTS"
channel_name = "insult_channel"

while True:
    insults = client.smembers(insult_list)
    for insult in insults:
        client.publish(channel_name, insult)  # Publica en el canal
        print(f"Broadcasted: {insult}")
    time.sleep(5)
