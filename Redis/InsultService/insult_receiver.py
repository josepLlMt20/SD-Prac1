import redis
from Redis.constants import INSULT_CHANNEL

# Escolta insults via publicació/subscripció

r = redis.Redis(decode_responses=True)
pubsub = r.pubsub()
pubsub.subscribe(INSULT_CHANNEL)

print("InsultReceiver escoltant...")
for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"Insult rebut: {message['data']}")