from Redis.insults_data import add_insult

insults = [
    "tonto", "idiota", "imbécil", "bobo", "cretino",
    "useless", "stupid", "fool", "dumb", "moron",
    "idiot", "jerk", "loser", "dimwit", "nitwit",
]

for insult in insults:
    added = add_insult(insult)
    print(f"{'✔️' if added else '❌'} {insult}")
