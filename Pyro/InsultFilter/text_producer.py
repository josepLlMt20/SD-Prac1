import Pyro4
import time

filter_service = Pyro4.Proxy("PYRONAME:FilterService")

texts = [
    "Hola, ¿cómo estás?",
    "Este es un texto sin insultos.",
    "Shai brait like a daimon",
    "Te mando un abrazo digital",
]

for text in texts:
    result = filter_service.filter(text)
    print(f"[PRODUCER] Enviado: {text}")
    time.sleep(1)
