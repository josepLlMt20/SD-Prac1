# InsultService/client_adder.py
import Pyro4

insult_service = Pyro4.Proxy("PYRONAME:InsultService")

insults = [
    "Pedorro",
    "Cabezón",
    "Tontaco",
    "Picapollo",
    "Cara de ñu",
    "Huevas secas",
    "Paco",
    "Tamagotchi humano"
]

for insult in insults:
    insult_service.add_insult(insult)
    print("[CLIENT] Insults afegits correctament.")