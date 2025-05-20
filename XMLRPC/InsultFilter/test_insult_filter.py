import xmlrpc.client
import time
import re
from threading import Thread

proxy = xmlrpc.client.ServerProxy("http://localhost:8010/")

def run_worker():
    while True:
        text = proxy.get_task()
        if not text:
            break
        insults = proxy.get_insults()
        filtered = text
        for insult in insults:
            pattern = re.compile(r'\b' + re.escape(insult) + r'\b', re.IGNORECASE)
            filtered = pattern.sub("CENSORED", filtered)
        proxy.submit_result(filtered)
        print(f"[Worker] Processat: {filtered}")

def test_insult_filter():
    print("[TEST] Afegint insults...")
    insults = ["tonto", "idiota", "imbécil", "bobo", "cretino"]
    for insult in insults:
        proxy.submit_insult(insult)
    print("[TEST] Insults afegits. ", proxy.get_insults())

    print("[TEST] Enviant textos...")
    texts = [
        "Eres un tonto integral.",
        "Mi jefe es un cretino.",
        "Hoy he hablado con un idiota.",
        "El cielo está azul.",
        "Qué bobo eres a veces.",
    ]
    for text in texts:
        proxy.submit_text(text)
        print(f"[TEST] Text enviat: {text}")

    # Iniciar el worker com a thread
    print("[TEST] Iniciant worker integrat...")
    worker_thread = Thread(target=run_worker)
    worker_thread.start()
    worker_thread.join()

    # Mostrar resultats
    print("[TEST] Resultats:")
    results = proxy.get_results()
    for r in results:
        print(f" - {r}")

    if any("CENSORED" in r for r in results):
        print("\n✅ Test passat correctament!")
    else:
        print("\n❌ Test fallat: cap text censurat.")

if __name__ == "__main__":
    test_insult_filter()
