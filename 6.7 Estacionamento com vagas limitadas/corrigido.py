import threading
import time
import random

CAPACIDADE = 5
# O Semáforo inicializa com o número de vagas. 
# Cada acquire() decrementa, cada release() incrementa.
vagas_disponiveis = threading.Semaphore(CAPACIDADE)
mutex_print = threading.Lock() # Apenas para organizar os logs no console

def veiculo_correto(id):
    print(f"🚗 Veículo {id} chegou e aguarda vaga...")
    
    # Se o semáforo for 0, a thread bloqueia aqui automaticamente
    vagas_disponiveis.acquire()
    
    with mutex_print:
        # O valor atual do semáforo nos diz quantas vagas restam
        # (Nota: em Python, _value acessa o contador interno para fins de log)
        ocupacao = CAPACIDADE - vagas_disponiveis._value
        print(f"✅ Veículo {id} ESTACIONOU. Ocupação atual: {ocupacao}/{CAPACIDADE}")

    time.sleep(random.uniform(1, 3)) # Simula o tempo que o carro fica parado

    with mutex_print:
        print(f"释放 Veículo {id} SAINDO...")
    
    # Devolve a vaga para o sistema, possivelmente acordando quem espera no acquire()
    vagas_disponiveis.release()

# Inicialização
for i in range(12):
    threading.Thread(target=veiculo_correto, args=(i,)).start()
    time.sleep(random.uniform(0.1, 0.4))