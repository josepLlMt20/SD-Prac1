import xmlrpc.client

server = xmlrpc.client.ServerProxy("http://localhost:8000/")

# Agregar insultos
print(server.add_insult("Eres más lento que un caracol en reversa."))
print(server.add_insult("Tienes menos carisma que un ladrillo."))

# Obtener la lista de insultos
print("Lista de insultos:", server.get_insults())

# Obtener un insulto aleatorio
print("Insulto aleatorio:", server.insult_me())
