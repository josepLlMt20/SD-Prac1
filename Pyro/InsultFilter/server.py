import Pyro4

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class FilterService:
    def __init__(self):
        self.results = []
        self.insults = {"pedorro", "cabezón", "tontaco", "paco", "picapollo", "mierdolo"}

    def filter(self, text):
        censored = []
        for word in text.split(): #això va paraula per paraula però abans no hem fet un que anava directament?
            clean = word.lower().strip(",.!?")  #això tampoc crec que calgui no?
            if clean in self.insults:
                censored.append("CENSORED")
            else:
                censored.append(word)
        result = " ".join(censored)
        self.results.append(result)
        print(f"[SERVER] Text filtrat: {result}")
        return result

    def get_results(self):
        return self.results

daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()

service = FilterService()
uri = daemon.register(service)
ns.register("FilterService", uri)

print("[SERVER] FilterService corrent la marato...")
daemon.requestLoop()
