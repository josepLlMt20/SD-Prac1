import Pyro4
from collections import deque

@Pyro4.expose
@Pyro4.behavior(instance_mode="session")
class FilterService:
    def __init__(self):
        self.queue = deque()
        self.results = []
        self.insults = {"pedorro", "cabezón", "tontaco", "paco", "picapollo", "mierdolo"}

    def submit_text(self, text):
        self.queue.append(text)
        print(f"[SERVER] Text rebut: {text}")
        return True

    def get_task(self):
        if self.queue:
            return self.queue.popleft()
        return None

    def submit_result(self, result):
        self.results.append(result)
        print(f"[SERVER] Resultat rebut: {result}")
        return True

    def get_results(self):
        return self.results

    def get_insults(self):
        return list(self.insults)

    def reset(self):
        self.queue.clear()
        self.results.clear()
        print("[SERVER] Resultats esborrats.")
        return True


daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()

service = FilterService()
uri = daemon.register(service)
ns.register("FilterService", uri)

print("[SERVER] FilterService corrent...")
daemon.requestLoop()
