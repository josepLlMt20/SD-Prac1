import redis
import time
import threading
import random
import re
from Redis.constants import TEXT_QUEUE, RESULT_LIST, INSULT_LIST
from Redis.insults_data import add_insult, get_insults

NUM_TASKS = 1000

def reset_redis():
    r = redis.Redis(decode_responses=True)
    r.delete(TEXT_QUEUE)
    r.delete(RESULT_LIST)
    r.delete(INSULT_LIST)
    insults = ["tonto", "idiota", "imbécil", "bobo", "cretino"]
    for insult in insults:
        add_insult(insult)

def generate_texts():
    r = redis.Redis(decode_responses=True)
    sujetos = ["Mi jefe", "El conductor", "Mi vecino", "Ese tipo", "El cliente"]
    acciones = ["es un", "parece un", "se comporta como un", "claramente es un"]
    insultos = ["tonto", "idiota", "imbécil", "bobo", "cretino"]
    for _ in range(NUM_TASKS):
        texto = f"{random.choice(sujetos)} {random.choice(acciones)} {random.choice(insultos)}."
        r.rpush(TEXT_QUEUE, texto)

def worker_loop(worker_id):
    r = redis.Redis(decode_responses=True)
    insults = get_insults()
    count = 0

    while True:
        try:
            result = r.blpop(TEXT_QUEUE, timeout=2)
            if not result:
                break
            _, texto = result
            filtrado = texto
            for insult in insults:
                pattern = re.compile(r'\b' + re.escape(insult) + r'\b', re.IGNORECASE)
                filtrado = pattern.sub("CENSORED", filtrado)
            r.rpush(RESULT_LIST, filtrado)
            count += 1
            time.sleep(0.005)
        except Exception as e:
            print(f"[Worker-{worker_id}] Error: {e}")

    print(f"[Worker-{worker_id}] Ha processat {count} textos.")

def run_scaling_test(num_workers):
    print(f"\n Test amb {num_workers} worker(s)...")
    reset_redis()
    generate_texts()

    threads = []
    start = time.time()

    for i in range(num_workers):
        t = threading.Thread(target=worker_loop, args=(i + 1,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    end = time.time()
    duration = end - start
    print(f"⏱ Temps total: {duration:.2f}s")
    return duration

if __name__ == "__main__":
    resultados = []
    for workers in [1, 2, 3]:
        duracion = run_scaling_test(workers)
        resultados.append((workers, duracion))

    print("\n Resultats:")
    for w, d in resultados:
        print(f"{w} workers ➝ {d:.2f}s")

    base = resultados[0][1]
    for w, d in resultados[1:]:
        print(f" Speedup amb {w} workers: {base/d:.2f}x")
