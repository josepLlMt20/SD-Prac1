import pandas as pd
import time

def save_results_to_excel(results, filename="resultados.xlsx"):
    df = pd.DataFrame(results)
    df.to_excel(filename, index=False)
    print(f"[✔] Resultados guardados en {filename}")

def measure_time(func, *args, **kwargs):
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()
    duration = end - start
    return result, duration
