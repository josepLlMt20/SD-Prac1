import xmlrpc.client
import time

proxy = xmlrpc.client.ServerProxy("http://localhost:8010/")

while True:
    results = proxy.get_results()
    print("[Viewer] Resultats filtrats:")
    for r in results:
        print(f" - {r}")
    time.sleep(10)