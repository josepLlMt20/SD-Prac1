# InsultService/receiver.py (FIXED)
import Pyro4

@Pyro4.expose
class Receiver:
    def notify(self, insult):
        print(f"[INSULT REBUT]: {insult}")

daemon = Pyro4.Daemon()
receiver = Receiver()
uri = daemon.register(receiver)

# CREAMOS UN PROXY del objeto local registrado
proxy = Pyro4.Proxy(uri)

insult_service = Pyro4.Proxy("PYRONAME:InsultService")
insult_service.subscribe(proxy)

print("[RECEIVER] Subscrit correctament. Esperant insults...")
daemon.requestLoop()
