import xmlrpc.client


def main():
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

    insults = [
        "Eres como un bucle infinito sin break.",
        "Tu lógica es más difusa que un else sin if.",
        "Tienes menos sentido del humor que un puntero nulo.",
        "Eres como un programa sin excepciones.",
        "Tu código es tan limpio como un archivo sin extensión.",
        "Eres como un bug en producción.",
        "Tu sentido del humor es tan raro como un puntero a void.",
        "Eres como un compilador sin errores."
    ]

    print("[ClientAdder] Afegint insults...")
    for insult in insults:
        success = proxy.add_insult(insult)
        if success:
            print(f"✅ Insult afegit: {insult}")
        else:
            print(f"⚠️  El insult existent a la cua: {insult}")

if __name__ == "__main__":
    main()
