import xmlrpc.client
import time

filter_proxy = xmlrpc.client.ServerProxy("http://localhost:8010/")
insult_proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

while True:
    text = filter_proxy.get_task()
    if text:
        insults = insult_proxy.get_insults()
        print(f"[Worker] Procesando: {text}")
        for insult in insults:
            text = text.replace(insult, "CENSORED")
        filter_proxy.submit_result(text)
        print(f"[Worker] Resultado enviado: {text}")
    else:
        time.sleep(1)
