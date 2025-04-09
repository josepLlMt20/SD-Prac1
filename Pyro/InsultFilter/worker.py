import Pyro4
import time

filter_service = Pyro4.Proxy("PYRONAME:FilterService")

# Simulació d'un loop que rebrà tasques
print("[WORKER] Llest per filtrar textos...")
while True:
    time.sleep(5)
