import xmlrpc.client
import time
import random

proxy = xmlrpc.client.ServerProxy("http://localhost:8010/")

texts = [
    "Hoy he hablado con un idiota en la cafetería.",
    "El cielo está azul, pero tú sigues siendo un bobo.",
    "Mi jefe es un auténtico estúpido.",
    "Qué tonto he sido al olvidar las llaves.",
    "Ese imbécil me empujó en la cola del cine.",
    "El cretino de mi vecino no para de hacer ruido.",
    "Ayer vi un cochino robando en la tienda.",
    "No seas un tarado y estudia para el examen.",
    "El partido fue un desastre por culpa de un cabrón.",
    "El niño se portó como un auténtico mierdolo.",
]

while True:
    t = random.choice(texts)
    proxy.submit_text(t)
    print(f"[ClientText] Enviado: {t}")
    time.sleep(5)
