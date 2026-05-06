import threading
import time
import random

# Configurações do ambiente
N_CADEIRAS = 3
CLIENTES_TOTAIS = 10

# Semáforos e Variáveis de Controle
clientes_esperando = threading.Semaphore(0)  # Clientes prontos para o corte
barbeiro_pronto = threading.Semaphore(0)     # Barbeiro disponível para atender
mutex = threading.Lock()                     # Protege o acesso às cadeiras
cadeiras_ocupadas = 0
def barbeiro():
    while True:
        # O barbeiro dorme até que um cliente chegue e o acorde
        clientes_esperando.acquire()
        
        # Bloqueia o acesso para atualizar o estado das cadeiras
        with mutex:
            global cadeiras_ocupadas
            cadeiras_ocupadas -= 1
        
        # Sinaliza que está pronto para cortar
        barbeiro_pronto.release()
        
        print(f"[BARBEIRO] Cortando cabelo... (Cadeiras ocupadas: {cadeiras_ocupadas})")
        time.sleep(random.uniform(0.5, 1.5))
        print("[BARBEIRO] Corte finalizado.")

def cliente(id):
    global cadeiras_ocupadas
    print(f"Cliente {id} chegou.")
    
    with mutex:
        if cadeiras_ocupadas < N_CADEIRAS:
            cadeiras_ocupadas += 1
            print(f"Cliente {id} sentou na espera. (Total: {cadeiras_ocupadas})")
            
            # Acorda o barbeiro
            clientes_esperando.release()
        else:
            print(f"Cliente {id} foi embora (Barbearia lotada).")
            return

    # Espera o barbeiro estar efetivamente livre para sentar na cadeira de corte
    barbeiro_pronto.acquire()
    print(f"Cliente {id} está cortando o cabelo.")

# Inicialização
t_barbeiro = threading.Thread(target=barbeiro, daemon=True)
t_barbeiro.start()

for i in range(CLIENTES_TOTAIS):
    threading.Thread(target=cliente, args=(i,)).start()
    time.sleep(random.uniform(0.1, 0.8))

time.sleep(5) # Tempo para finalizar as execuções no log