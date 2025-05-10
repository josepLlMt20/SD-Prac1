# InsultService/server.py con tu estilo
import Pyro4
import threading
import time
import random

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")

# Crea un servei anomenat InsultService. Té llista d'insults i llista de subscriptors
class InsultService:
    def __init__(self):
        self.insults = set()
        self.subscribers = []

    def add_insult(self, insult):
        if insult not in self.insults:
            self.insults.add(insult)
            print(f"[SERVER] Insult afegit: {insult}")
            return True
        return False

    def get_insults(self):
        return list(self.insults)

    def subscribe(self, callback):
        self.subscribers.append(callback)
        return "Subscrit correctament."

    # Cada 5 segons, selecciona un insult aleatori i el reenvia a tots els subscriptors
    def start_broadcasting(self):
        def loop():
            while True:
                if self.insults and self.subscribers:
                    insult = random.choice(list(self.insults))
                    for sub in self.subscribers:
                        try:
                            sub.notify(insult)
                        except Exception as e:
                            print(f"[SERVER] Error notificant: {e}")
                time.sleep(5)

        threading.Thread(target=loop, daemon=True).start()

# 👇 Estilo MyRemoteObject aquí
service = InsultService()
service.start_broadcasting()

daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(service)
ns.register("InsultService", uri)

print("Servidor InsultService corrent...")
daemon.requestLoop()
