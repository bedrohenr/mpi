import math
import numpy as np
from mpi4py import MPI 

def isQuadradoPerfeito(num):
    """
    Verifica se um número é um quadrado perfeito de forma eficiente.
    A lógica permanece a mesma, pois é uma função local.
    """
    if num < 0:
        return False
    if num == 0 or num == 1:
        return True 

    raiz = math.isqrt(num)

    return raiz * raiz == num

def calcular_quadrados_locais(bloco_local):
    """
    Calcula a contagem de quadrados perfeitos em uma fatia de dados local.

    Args:
        bloco_local (np.ndarray): A fatia do vetor (chunk) recebida via MPI.

    Returns:
        int: O número de quadrados perfeitos encontrados no bloco.
    """
    quadrados_encontrados = 0 
    
    # O bloco_local já é a fatia que o processo deve processar.
    for numero in bloco_local:
        if isQuadradoPerfeito(int(numero)): 
            quadrados_encontrados += 1
            
    return quadrados_encontrados

if __name__ == '__main__':
    
    # Obtém o comunicador principal (o universo de processos)
    comm = MPI.COMM_WORLD
    # Obtém o ID (rank) do processo atual (0 para o Mestre)
    rank = comm.Get_rank()
    # Obtém o número total de processos (tamanho do comunicador)
    size = comm.Get_size()

    # Vetor de Dados
    LISTA = None
    if rank == 0:
        # Apenas o processo Mestre (rank 0) carrega os dados
        try:
            LISTA = np.load('P.npy')
            N = len(LISTA)
            print(f"Número total de elementos no vetor: {N}")
        except FileNotFoundError:
            print("Erro: Arquivo 'P.npy' não encontrado no diretório.")
            exit()
    else:
        # Os processos Escravos precisam de 'N' para calcular o tamanho do bloco.
        N = 0
        
    # O Mestre distribui o tamanho total do vetor para todos os Escravos
    N = comm.bcast(N, root=0)

    # Calcula o tamanho do bloco que CADA processo deve receber.
    # Usamos divisões inteiras e o resto é distribuído nos primeiros processos.
    tamanho_base_bloco = N // size
    resto = N % size
    
    # Calcula o tamanho do bloco local para o processo atual (rank)
    tamanho_bloco_local = tamanho_base_bloco + (1 if rank < resto else 0)

    # Variável para receber o bloco de dados localmente (todos os processos)
    bloco_local = np.empty(tamanho_bloco_local, dtype=LISTA.dtype if LISTA is not None else np.int64) 

    # Criação dos parâmetros para Scatterv (necessário para blocos de tamanhos desiguais)
    if rank == 0:
        # O Mestre calcula os tamanhos e os deslocamentos de cada bloco
        counts = [tamanho_base_bloco + (1 if i < resto else 0) for i in range(size)]
        displs = [sum(counts[:i]) for i in range(size)]
    else:
        # Os Escravos não precisam calcular, mas precisam das variáveis.
        counts = None
        displs = None
        
    # comm.Barrier() # Garante que todos os processos estejam prontos antes de começar a cronometrar
    
    # tempo_inicio = time.time()
    
    # Scatterv: Distribui fatias de tamanhos desiguais do LISTA (no Mestre) para
    # o bloco_local em cada processo, usando counts e displs como mapa.
    comm.Scatterv([LISTA, counts, displs, MPI.INT], bloco_local, root=0)

    # Execução Local
    
    # O processo local calcula a sua contagem
    contagem_local = calcular_quadrados_locais(bloco_local)
    
    # Agregação dos Resultados (Reduce)
    
    # Reduce: Soma todas as 'contagem_local' no 'contagem_total' do Mestre (root=0).
    contagem_total = comm.reduce(contagem_local, op=MPI.SUM, root=0)
    
    # comm.Barrier() # Garante que todos os processos completaram antes de parar a cronometragem
    
    # tempo_fim = time.time()
    
    # --- RESULTADOS E CÁLCULO DE SPEEDUP ---

    if rank == 0:
        # tempo_paralelo = tempo_fim - tempo_inicio
        
        # # Cálculo do Speedup: S = Tempo Sequencial / Tempo Paralelo
        # speedup = tempo_referencia / tempo_paralelo
        
        # print("\n--- Resultados MPI ---")
        # print(f"Tempo Sequencial (Referência): {tempo_referencia:.7f}s")
        # print(f"Tempo Paralelo ({size} processos): {tempo_paralelo:.7f}s")
        # print(f"Speedup: {speedup:.4f}")
        # print(f"Quantidade de quadrados perfeitos: {contagem_total}")
        
        # # 2. retorno(Print no console, numérico): quantidade de quadrados perfeitos
        # # Para satisfazer o requisito estrito de retorno (somente o número)
        # print(f"\nRetorno exigido pelo exercício:\n{contagem_total}")

        # # Verifica o critério de Speedup
        # if speedup > 1:
        #     print(f"\n✅ Critério de Speedup > 1 atendido ({speedup:.4f} > 1).")
        # else:
        #     print(f"\n❌ Critério de Speedup > 1 NÃO atendido.")

        # 2. retorno(Print no console, numérico): quantidade de quadrados perfeitos
        # Para satisfazer o requisito estrito de retorno (somente o número)
        print(f"\nRetorno exigido pelo exercício:\n{contagem_total}")