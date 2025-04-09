import xmlrpc.client
import time
import random

proxy = xmlrpc.client.ServerProxy("http://localhost:8010/")
texts = [
    "Eres como un bucle infinito sin break.",
    "Tu logica es mas difusa que un else sin if.",
    "Eres como un error 404: no te encuentro por ninguna parte.",
    "Tu inteligencia es como un puntero nulo: no tiene direccion.",
    "Eres como un programa sin excepciones: no tienes sentido.",
    "Tu codigo es como un bucle sin fin: nunca termina.",
    "Eres como un compilador sin errores: no existes.",
    "Tu sentido del humor es como un stack overflow: fuera de control.",
    "Eres como un script sin permisos: no tienes acceso a nada.",
    "Tu logica es como un algoritmo de ordenamiento: desordenada.",
]

while True:
    t = random.choice(texts)
    proxy.submit_text(t)
    print(f"[ClientAngry] Enviado: {t}")
    time.sleep(3)