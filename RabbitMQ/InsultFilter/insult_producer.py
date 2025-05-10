import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue='insult_queue')

insults = [
    "inútil",
    "cenicero",
    "ficción",
    "caracol",
    "cojo",
    "café",
    "basurero",
    "torpe",
    "bicicleta",
    "papel",
    "aburrido",
    "hierba"
]

# Envia una llista d'insults a la cua d'insults i filter.py els recull i guarda a memòria
for insult in insults:
    channel.basic_publish(exchange='', routing_key='insult_queue', body=insult)
    print(f"[InsultProducer] Insult enviat: {insult}")

connection.close()
