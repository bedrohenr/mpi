import numpy as np
from mpi4py import MPI
import time
import math


def is_prime(n):
    """
    Verifica se um número é primo.
    Implementação otimizada.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    # verificar divisores até a raiz quadrada de n
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def count_primes_in_array(arr):
    """
    Conta o número de primos em um array NumPy.
    Aplica a função is_prime() a todos os elementos.
    """
    # Usa a vetorização do NumPy com a função is_prime
    # np.vectorize transforma uma função Python em uma "função universal" NumPy.
    prime_check = np.vectorize(is_prime)
    
    # Retorna a soma booleana (True conta como 1, False como 0)
    return np.sum(prime_check(arr))

# --- Lógica MPI Principal ---

# Inicializa o MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Nome do arquivo de entrada
FILE_NAME = 'P.npy'

# O Rank 0 lida com a leitura, distribuição e agregação dos resultados.
if rank == 0:
    # Carregando o arquivo
    data = np.load(FILE_NAME)

    total_elements = len(data)
    
    # 2. Cálculo do Tamanho do Subconjunto para cada Processo
    
    # Calcula o número base de elementos por processo
    # total_elements // size: divisão inteira
    base_count = total_elements // size
    
    # Calcula o número de elementos restantes que devem ser distribuídos
    # entre os primeiros `remainder` processos
    remainder = total_elements % size
    
    # Cria uma lista de contagens (elementos por processo)
    # Ex: para 10 elementos e 3 processos: [4, 3, 3]
    counts = [base_count + 1 if i < remainder else base_count for i in range(size)]
    
    # Cria uma lista de deslocamentos (onde começa o subconjunto de cada processo)
    # Ex: para [4, 3, 3]: [0, 4, 7]
    displacements = [sum(counts[:i]) for i in range(size)]
    
    print(f"\n--- Início do Processamento Paralelo ---")
    print(f"Total de processos: {size}")
    print(f"Total de elementos: {total_elements}")
    start_time = time.time()
    
    # O Rank 0 precisa de espaço para receber seus próprios dados
    # O bloco de dados do Rank 0 é o primeiro (tamanho = counts[0])
    local_data = np.empty(counts[0], dtype=data.dtype)
    
else:
    # Processos escravos (Rank > 0)
    # Inicializa variáveis para o Broadcast (tamanho e tipo de dados)
    data = None
    counts = None
    displacements = None
    total_elements = None

# 3. Broadcast dos Parâmetros de Distribuição
# Todos os processos precisam saber o esquema de distribuição
counts = comm.bcast(counts, root=0)
displacements = comm.bcast(displacements, root=0)
total_elements = comm.bcast(total_elements, root=0)

# O tamanho do subconjunto local para o processo atual
local_count = counts[rank]

# Cria o buffer de recebimento para o processo atual (se ainda não tiver sido criado)
if rank != 0:
    local_data = np.empty(local_count, dtype=np.int64) 
    
# 4. Distribuição do Array (Scatterv)
# Scatterv é usado porque os subconjuntos de dados podem ter tamanhos diferentes
comm.Scatterv([data, counts, displacements, MPI.LONG], local_data, root=0)

# 5. Processamento Local (Contagem de Primos)
local_prime_count = count_primes_in_array(local_data)

# 6. Agregação dos Resultados (Reduce)
# Soma as contagens locais de todos os processos no Rank 0
local_prime_count64 = np.int64(local_prime_count)
total_prime_count = comm.reduce(local_prime_count64, op=MPI.SUM, root=0)

# 7. Exibição do Resultado (Apenas Rank 0)
if rank == 0:
    print(f"Total de números primos no arquivo: {total_prime_count}")
    print(f"--- Fim do Processamento Paralelo ---\n")