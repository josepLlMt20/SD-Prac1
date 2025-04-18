from RabbitMQ.constants import RESULT_LIST_FILE

# Mostra els texts filtrats

print("Filtered Results:")
try:
    with open(RESULT_LIST_FILE, "r") as f:
        for line in f:
            print(f"- {line.strip()}")
except FileNotFoundError:
    print("No results yet.")