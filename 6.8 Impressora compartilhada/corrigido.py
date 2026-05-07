import threading
import queue
import time
import random

# Fila de impressão (Thread-Safe por padrão)
fila_impressao = queue.Queue()

def trabalhador_impressora():
    """Este é o 'Daemon' da impressora que processa a fila."""
    while True:
        # Bloqueia até que algo entre na fila
        documento, id_proc = fila_impressao.get()
        
        print(f"\n--- Iniciando Trabalho (Processo {id_proc}) ---")
        for char in documento:
            print(char, end="", flush=True)
            time.sleep(0.05)
        print(f"\n--- Fim do Trabalho (Processo {id_proc}) ---")
        
        # Sinaliza que a tarefa da fila foi concluída
        fila_impressao.task_done()

def processo_usuario(id, texto):
    print(f"Usuário {id} enviando documento para a fila...")
    fila_impressao.put((texto, id))

# 1. Iniciamos o serviço de impressão (consumidor)
t_impressora = threading.Thread(target=trabalhador_impressora, daemon=True)
t_impressora.start()

# 2. Vários usuários enviam documentos (produtores)
mensagens = ["ESTE É O DOC 1", "segundo arquivo aqui", "ULTIMO TESTE"]
for i, msg in enumerate(mensagens):
    threading.Thread(target=processo_usuario, args=(i+1, msg)).start()
    time.sleep(random.uniform(0.01, 0.1))

# Aguarda todos os itens da fila serem processados
fila_impressao.join()
print("\n[SISTEMA] Todos os documentos foram impressos com sucesso.")