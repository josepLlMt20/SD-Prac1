import Pyro4

# Conectar con el Observable Server
observable = Pyro4.Proxy("PYRONAME:example.observable")

# Enviar una notificación a los observadores
observable.notify_observers("¡Nuevo evento en el servidor!")
