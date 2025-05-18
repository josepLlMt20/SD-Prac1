import Pyro4
import time

filter_service = Pyro4.Proxy("PYRONAME:FilterService")

texts = [
    "Hola, ¿cómo estás?",
    "Este es un texto sin insultos.",
    "Shai brait like a daimon",
    "Te mando un abrazo digital",
]

# Envia textos sense insults al FilterService
for text in texts:
    result = filter_service.submit_text(text)
    print(f"[PRODUCER] Enviat: {text}")
    time.sleep(1)
