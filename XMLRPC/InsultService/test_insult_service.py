import xmlrpc.client
import time

# Connexió al servei
proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
receiver_url = "http://localhost:8002/"

# Test: Afegir insults
print("[TEST] Afegint insults...")
added = proxy.add_insult("Ets més lent que un bucle infinit.")
print(f" - Afegit nou insult: {added}")
added = proxy.add_insult("Ets més lent que un bucle infinit.")
print(f" - Reintent duplicat (ha de ser False): {added}")

# Test: Obtenir insults
print("[TEST] Obtenint insults...")
insults = proxy.get_insults()
print(f" - Total insults: {len(insults)}")
print(f" - Exemple: {insults[:3]}")

# Test: Registrar receiver
print("[TEST] Registrant receiver...")
result = proxy.register_receiver(receiver_url)
print(f" - Receiver registrat: {result}")

# Test: Broadcast manual
print("[TEST] Broadcast manual (1 insult)...")
if insults:
    proxy.broadcast_insult(insults[0])
    print(" - Broadcast enviat (comprova consola del receiver).")
else:
    print(" - No hi ha insults disponibles per enviar.")

print("\n✅ TEST FINALITZAT. Revisa consola del receiver per veure missatge rebuts.")
