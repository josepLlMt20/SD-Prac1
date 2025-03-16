import Pyro4

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")  # Modo singleton para compartir estado
class Observable:
    def __init__(self):
        self.observers = []

    def register_observer(self, observer_uri):
        self.observers.append(observer_uri)
        return f"Observador {observer_uri} registrado."

    def unregister_observer(self, observer_uri):
        self.observers.remove(observer_uri)
        return f"Observador {observer_uri} eliminado."

    def notify_observers(self, message):
        for observer_uri in self.observers:
            observer = Pyro4.Proxy(observer_uri)
            observer.update(message)

# Configuración del servidor
daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(Observable())
ns.register("example.observable", uri)

print("Observable Server corriendo...")
daemon.requestLoop()
