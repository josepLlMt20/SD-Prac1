import xmlrpc.client
import time
import random

proxy = xmlrpc.client.ServerProxy("http://localhost:8010/")
texts = [
    "El cielo esta azul.",
    "Hoy es un buen dia para programar.",
    "Me gusta el helado.",
    "La vida es bella.",
    "El sol brilla.",
    "La luna es hermosa.",
    "Los gatos son adorables.",
    "Los perros son leales.",
    "El mar es profundo.",
]

while True:
    t = random.choice(texts)
    proxy.submit_text(t)
    print(f"[ClientText] Enviado: {t}")
    time.sleep(5)
