# InsultService/server.py
import sys
import Pyro4
import threading
import time
import random

@Pyro4.expose
@Pyro4.behavior(instance_mode="session")
class InsultService:
    def __init__(self):
        self.insults = set()
        self.subscribers = []

    def add_insult(self, insult):
        if insult not in self.insults:
            self.insults.add(insult)
            print(f"[{self._name}] Insult afegit: {insult}")
            return True
        return False

    def get_insults(self):
        return list(self.insults)

    def subscribe(self, callback):
        self.subscribers.append(callback)
        return "Subscrit correctament."

    def start_broadcasting(self):
        def loop():
            while True:
                if self.insults and self.subscribers:
                    insult = random.choice(list(self.insults))
                    for sub in self.subscribers:
                        try:
                            sub.notify(insult)
                        except Exception as e:
                            print(f"[{self._name}] Error notificant: {e}")
                time.sleep(5)
        threading.Thread(target=loop, daemon=True).start()

if __name__ == "__main__":
    node_name = sys.argv[1] if len(sys.argv)>1 else "InsultService1"

    service = InsultService()
    service._name = node_name
    service.start_broadcasting()

    daemon = Pyro4.Daemon(host="localhost")
    ns     = Pyro4.locateNS()
    uri    = daemon.register(service)
    ns.register(node_name, uri)

    print(f"[{node_name}] Servidor corriendo en URI: {uri}")
    daemon.requestLoop()
