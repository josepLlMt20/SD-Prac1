import xmlrpc.client
import time

NUM_REQUESTS = 250

proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

start_time = time.time()

for i in range(NUM_REQUESTS):
    try:
        proxy.add_insult(f"Insult number {i}")
    except Exception as e:
        print(f"Request failed: {e}")

end_time = time.time()
total_time = end_time - start_time
rps = NUM_REQUESTS / total_time

print(f"InsultService Stress Test:")
print(f"Total requests: {NUM_REQUESTS}")
print(f"Total time: {total_time:.2f} seconds")
print(f"Requests per second (RPS): {rps:.2f}")
