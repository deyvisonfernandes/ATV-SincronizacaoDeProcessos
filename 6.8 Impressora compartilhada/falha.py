import threading
import time
import random

def impressora_falha(documento, id_processo):
    print(f"\n[IMPRESSORA] Processo {id_processo} iniciou a impressão...")
    for caractere in documento:
        # Simula o tempo de impressão de cada caractere
        print(caractere, end="", flush=True)
        time.sleep(random.uniform(0.01, 0.05))
    print(f"\n[IMPRESSORA] Processo {id_processo} finalizou.")

# Simulação de múltiplos processos enviando dados ao mesmo tempo
docs = [
    ("AAAAAAAAAA", 1),
    ("bbbbbbbbbb", 2),
    ("CCCCCCCCCC", 3)
]

for d, i in docs:
    threading.Thread(target=impressora_falha, args=(d, i)).start()