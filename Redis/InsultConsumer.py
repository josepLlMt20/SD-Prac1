import redis

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

queue_name = "insult_queue"
insult_list = "INSULTS"

while True:
    insult = client.blpop(queue_name, timeout=0)  # Espera un insulto
    if insult:
        insult_text = insult[1]
        if not client.sismember(insult_list, insult_text):  # Solo agrega si es nuevo
            client.sadd(insult_list, insult_text)
            print(f"Stored: {insult_text}")
