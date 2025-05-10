import Pyro4
import time

filter_service = Pyro4.Proxy("PYRONAME:FilterService")

texts = [
    "Ese paco es un cabezón tremendo",
    "Pedorro picapollo tontaco",
    "No puedo con tanto tontaco junto",
    "Qué pedorro más grande, Josep",
]

# Envia textos amb insults al Filter Service per a que els filtri
for text in texts:
    result = filter_service.filter(text)
    print(f"[PRODUCER] Enviat: {text}")
    time.sleep(1) # cal?
