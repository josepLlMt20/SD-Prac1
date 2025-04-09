import Pyro4
import time

filter_service = Pyro4.Proxy("PYRONAME:FilterService")

results = filter_service.get_results()
print("[Viewer] Resultados filtrados:")
for r in results:
    print(f" - {r}")
time.sleep(10)