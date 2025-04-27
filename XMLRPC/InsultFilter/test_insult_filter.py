import xmlrpc.client
import time
import re

def test_insult_filter():
    print("[Test] Iniciant test d'InsultFilter...")
    proxy = xmlrpc.client.ServerProxy("http://localhost:8010/")

    # 1. Afegir insults
    insults = ["tonto", "idiota", "imbécil", "bobo"]
    for insult in insults:
        proxy.submit_insult(insult)
        print(f"[Test] Insult afegit: {insult}")

    # 2. Enviar textos
    texts = [
        "Hoy he hablado con un idiota en la cafetería.",
        "El cielo está azul.",
        "Ese bobo no sabía qué hacer.",
        "Qué tonto soy!",
        "Me gusta el helado.",
        "El imbécil de turno no apareció."
    ]

    for text in texts:
        proxy.submit_text(text)
        print(f"[Test] Text enviat: {text}")

    # 3. Llançar Worker manualment
    while True:
        task = proxy.get_task()
        if task:
            insults_list = proxy.get_insults()
            filtered = task
            for insult in insults_list:
                pattern = re.compile(r'\b' + re.escape(insult) + r'\b', re.IGNORECASE)
                filtered = pattern.sub("CENSORED", filtered)
            proxy.submit_result(filtered)
            print(f"[Worker] Text filtrat: {filtered}")
        else:
            break  # No més textos a processar

    # 4. Recuperar resultats
    results = proxy.get_results()
    print("\n[Test] Resultats Finals:")
    for result in results:
        print(f" - {result}")

    # 5. Comprovar que hi ha textos censurats
    censored = any("CENSORED" in res for res in results)
    if censored:
        print("\n✅ Test passat correctament!")
    else:
        print("\n❌ Test fallat: no s'ha censurat res.")

if __name__ == "__main__":
    test_insult_filter()
