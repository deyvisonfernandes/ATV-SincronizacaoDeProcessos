import threading
import time
import random

class PonteControle:
    def __init__(self):
        self.monitor = threading.Condition()
        self.sentido_atual = None
        self.veiculos_atravessando = 0
        self.fila_espera = {"NORTE": 0, "SUL": 0}
        self.passagens_consecutivas = 0
        self.LIMITE_FLUXO = 3 # Evita que um lado domine a ponte para sempre

    def entrar_na_ponte(self, id, sentido):
        with self.monitor:
            self.fila_espera[sentido] += 1
            
            # Condição para esperar:
            # 1. Ponte ocupada por sentido oposto
            # OR 2. Limite de fluxo atingido enquanto o outro lado espera
            sentido_oposto = "SUL" if sentido == "NORTE" else "NORTE"
            
            while (self.sentido_atual is not None and self.sentido_atual != sentido) or \
                  (self.passagens_consecutivas >= self.LIMITE_FLUXO and self.fila_espera[sentido_oposto] > 0):
                self.monitor.wait()

            # Entrada na ponte
            self.fila_espera[sentido] -= 1
            self.sentido_atual = sentido
            self.veiculos_atravessando += 1
            self.passagens_consecutivas += 1
            print(f"[PONTE] Veículo {id} ({sentido}) entrou. (Ativos: {self.veiculos_atravessando})")

    def sair_da_ponte(self, id, sentido):
        with self.monitor:
            self.veiculos_atravessando -= 1
            print(f"[PONTE] Veículo {id} ({sentido}) saiu.")
            
            if self.veiculos_atravessando == 0:
                # Se o fluxo atual atingiu o limite ou a fila acabou, troca o sentido
                sentido_oposto = "SUL" if sentido == "NORTE" else "NORTE"
                if self.passagens_consecutivas >= self.LIMITE_FLUXO or self.fila_espera[sentido] == 0:
                    self.sentido_atual = None
                    self.passagens_consecutivas = 0
                
                self.monitor.notify_all()

def veiculo(id, sentido, ponte):
    ponte.entrar_na_ponte(id, sentido)
    time.sleep(random.uniform(0.3, 0.7)) # Tempo de travessia
    ponte.sair_da_ponte(id, sentido)

# Execução Corrigida
ponte_segura = PonteControle()
for i in range(10):
    s = "NORTE" if i < 5 else "SUL" # Força acúmulo de um lado para testar inanição
    threading.Thread(target=veiculo, args=(i, s, ponte_segura)).start()
    time.sleep(0.1)