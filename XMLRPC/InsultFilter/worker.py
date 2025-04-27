import xmlrpc.client
import time
import re

filter_proxy = xmlrpc.client.ServerProxy("http://localhost:8010/")

while True:
    text = filter_proxy.get_task()
    if text:
        insults = filter_proxy.get_insults()
        print(f"[Worker] Procesando: {text}")
        filtered = text

        for insult in insults:
            # Substitueix la paraula exacta
            pattern = re.compile(r'\b' + re.escape(insult) + r'\b', re.IGNORECASE)
            filtered = pattern.sub("CENSORED", filtered)

        filter_proxy.submit_result(filtered)
        print(f"[Worker] Resultado enviado: {filtered}")
    else:
        time.sleep(0.1)
