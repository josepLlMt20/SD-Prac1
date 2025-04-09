import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
proxy.add_insult("Eres como un bucle infinito sin break.")
proxy.add_insult("Tu logica es mas difusa que un else sin if.")
proxy.add_insult("Tienes menos sentido del humor que un puntero nulo.")
proxy.add_insult("Eres como un programa sin excepciones.")
proxy.add_insult("Tu codigo es tan limpio como un archivo sin extension.")
proxy.add_insult("Eres como un bug en producción.")
proxy.add_insult("Tu sentido del humor es tan raro como un puntero a void.")
proxy.add_insult("Eres como un compilador sin errores.")
print(proxy.get_insults())