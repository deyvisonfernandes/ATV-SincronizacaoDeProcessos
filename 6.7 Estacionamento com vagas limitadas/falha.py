import threading
import time
import random

VAGAS_TOTAIS = 5
vagas_ocupadas = 0

def veiculo_falho(id):
    global vagas_ocupadas
    
    print(f"🚗 Veículo {id} tentando entrar...")
    
    if vagas_ocupadas < VAGAS_TOTAIS:
        # Delay artificial para expor a Condição de Corrida (Race Condition)
        # Vários veículos lerão o mesmo valor de 'vagas_ocupadas' antes do incremento
        time.sleep(random.uniform(0.1, 0.3))
        
        vagas_ocupadas += 1
        print(f"✅ Veículo {id} ENTROU. Vagas ocupadas: {vagas_ocupadas}/{VAGAS_TOTAIS}")
        
        time.sleep(random.uniform(1, 2)) # Tempo de permanência
        
        vagas_ocupadas -= 1
        print(f"释放 Veículo {id} SAIU. Vagas ocupadas: {vagas_ocupadas}/{VAGAS_TOTAIS}")
    else:
        print(f"❌ Veículo {id} deu meia volta: Estacionamento Lotado!")

# Simulação com 10 veículos para 5 vagas
threads = []
for i in range(10):
    t = threading.Thread(target=veiculo_falho, args=(i,))
    threads.append(t)
    t.start()