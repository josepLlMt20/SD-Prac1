import redis
import time
import threading
import random
import re
from Redis.constants import TEXT_QUEUE, RESULT_LIST, INSULT_LIST
from Redis.insults_data import add_insult, get_insults
from StressTests.data_manager import guardar_resultats
from datetime import datetime

WORKERS = [1, 2, 3]
TASK_SIZES = [1000, 2500, 5000, 10000]

def reset_redis():
    r = redis.Redis(decode_responses=True)
    r.delete(TEXT_QUEUE)
    r.delete(RESULT_LIST)
    r.delete(INSULT_LIST)
    insults = ["tonto", "idiota", "imbécil", "bobo", "cretino"]
    for insult in insults:
        add_insult(insult)

def generate_texts(num_texts):
    r = redis.Redis(decode_responses=True)
    sujetos = ["Mi jefe", "El conductor", "Mi vecino", "Ese tipo", "El cliente"]
    acciones = ["es un", "parece un", "se comporta como un", "claramente es un"]
    insultos = ["tonto", "idiota", "imbécil", "bobo", "cretino"]
    for _ in range(num_texts):
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

def run_scaling_test(num_workers, num_tasks):
    print(f"\n Test amb {num_workers} worker(s) i {num_tasks} textos...")
    reset_redis()
    generate_texts(num_tasks)

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
    all_data = []

    for task_size in TASK_SIZES:
        results = []
        for workers in WORKERS:
            duracio = run_scaling_test(workers, task_size)
            results.append((workers, duracio))

        base_time = results[0][1]
        print(f"\n📊 Resultats amb {task_size} textos:")
        for w, d in results:
            speedup = base_time / d if w > 1 else 1.0
            print(f" • {w} worker(s): {d:.2f}s → {speedup:.2f}x")
            all_data.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Test": "InsultFilter",
                "Middleware": "Redis",
                "Mode": "Multi-node",
                "Clients": w,
                "Num Tasks": task_size,
                "Temps Total (s)": round(d, 2),
                "Speedup": round(speedup, 2)
            })

    guardar_resultats(all_data, sheet_name="Redis_Multi_Filter")
