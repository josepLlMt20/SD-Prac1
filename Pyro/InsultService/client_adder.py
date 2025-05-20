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

# Afegeix insults a la llista del servidor Pyro
for insult in insults:
    insult_service.add_insult(insult)
    print("[CLIENT] Insults afegits correctament.")