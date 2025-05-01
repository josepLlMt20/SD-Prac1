import redis
import time
import random
from Redis.constants import TEXT_QUEUE

r = redis.Redis(decode_responses=True)

sujetos = [
    "Mi jefe", "El conductor", "Mi compañero de trabajo", "Ese tipo", "El profesor",
    "El alumno", "Mi vecino", "El cliente", "El desconocido", "Él", "Ella"
]

insultos = [
    "tonto", "idiota", "imbécil", "bobo", "cretino",
    "inútil", "estúpido", "payaso", "burro", "menso",
    "torpe", "patán", "fracasado", "corto", "zoquete"
]

acciones = [
    "se comporta como un", "habla como un", "parece un", "claramente es un", "no es más que un"
]

i = 0
while True:
    sujeto = random.choice(sujetos)
    insulto = random.choice(insultos)
    accion = random.choice(acciones)
    texto = f"{sujeto} {accion} {insulto}."
    r.rpush(TEXT_QUEUE, texto)
    print(f"Produit (amb insult): {texto}")
    i += 1
    time.sleep(5)
