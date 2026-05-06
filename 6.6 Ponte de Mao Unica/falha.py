import threading
import time
import random

ponte_ocupada = False
veiculos_na_ponte = 0

def veiculo_falho(id, sentido):
    global ponte_ocupada, veiculos_na_ponte
    
    print(f"Veículo {id} ({sentido}) chegou na ponte.")
    
    # FALHA: Verificação sem trava (Race Condition)
    if not ponte_ocupada:
        # Pequeno delay para forçar a preempção e expor a falha
        time.sleep(0.1) 
        ponte_ocupada = True
        veiculos_na_ponte += 1
        
        print(f" >>> PERIGO: Veículo {id} ({sentido}) ENTROU na ponte!")
        time.sleep(0.5) # Atravessando
        
        veiculos_na_ponte -= 1
        if veiculos_na_ponte == 0:
            ponte_ocupada = False
        print(f" <<< Veículo {id} ({sentido}) SAIU da ponte.")
    else:
        print(f"Veículo {id} ({sentido}) aguardando...")

# Simulação da falha
sentidos = ["NORTE", "SUL"]
for i in range(5):
    t = threading.Thread(target=veiculo_falho, args=(i, random.choice(sentidos)))
    t.start()