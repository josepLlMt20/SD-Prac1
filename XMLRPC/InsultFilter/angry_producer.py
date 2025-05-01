import xmlrpc.client
import time
import random

proxy = xmlrpc.client.ServerProxy("http://localhost:8010/")
texts = [
    "Tonto",
    "Idiota",
    "Imbécil",
    "Estúpido",
    "Cretino",
    "Bobo",
    "Tarado",
    "Lelo",
    "Cagarruta",
    "Cabrón",
    "Mierdolo",
    "Cochino",
]

while True:
    t = random.choice(texts)
    proxy.submit_insult(t)
    print(f"[ClientAngry] Enviat: {t}")
    time.sleep(3)