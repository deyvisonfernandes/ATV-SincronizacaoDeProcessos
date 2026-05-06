import threading
import time
import random

cadeiras_ocupadas = 0
N_CADEIRAS = 3

def barbeiro_falho():
    global cadeiras_ocupadas
    while True:
        if cadeiras_ocupadas > 0:
            print(f"[BARBEIRO] Iniciando corte. Cadeiras antes: {cadeiras_ocupadas}")
            time.sleep(0.5) # Simula tempo de corte
            cadeiras_ocupadas -= 1
            print(f"[BARBEIRO] Corte terminado. Cadeiras agora: {cadeiras_ocupadas}")
        else:
            # O barbeiro fica em "Busy Waiting" (espera ocupada), consumindo CPU
            pass

def cliente_falho(id):
    global cadeiras_ocupadas
    print(f"Cliente {id} chegou.")
    
    # Simula a verificação de cadeiras sem proteção (Race Condition)
    if cadeiras_ocupadas < N_CADEIRAS:
        # Pausa proposital para aumentar a chance de preempção e evidenciar a falha
        time.sleep(random.uniform(0.1, 0.3)) 
        cadeiras_ocupadas += 1
        print(f"Cliente {id} sentou. Cadeiras ocupadas: {cadeiras_ocupadas}")
    else:
        print(f"Cliente {id} foi embora (Lotado).")

# Execução da Versão Falha
t_barbeiro = threading.Thread(target=barbeiro_falho, daemon=True)
t_barbeiro.start()

for i in range(10):
    threading.Thread(target=cliente_falho, args=(i,)).start()
    time.sleep(0.1)