import Pyro4

@Pyro4.expose
class Observer:
    def update(self, message):
        print(f"Notificación recibida: {message}")

daemon = Pyro4.Daemon()
uri = daemon.register(Observer())

# Conectar con el servidor y registrarse como observador
ns = Pyro4.locateNS()
observable = Pyro4.Proxy(ns.lookup("example.observable"))
observable.register_observer(uri)

print("Observador en espera de notificaciones...")
daemon.requestLoop()
