import numpy as np
from mpi4py import MPI
import time
import math

def ehPerfeito(n):
    if n < 2:
        return False
    soma = 1
    limite = int(math.sqrt(n))
    for i in range(2, limite + 1):
        if n % i == 0:
            soma += i
            outro = n // i
            if outro != i:
                soma += outro
    return soma == n

def contarPerfeitos(arr):
    check = np.vectorize(ehPerfeito)
    return np.sum(check(arr))

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

FILE_NAME = 'T.npy'

if rank == 0:
    data = np.load(FILE_NAME)

    total_elements = len(data)
    base_count = total_elements // size
    remainder = total_elements % size

    counts = [base_count + 1 if i < remainder else base_count for i in range(size)]
    displacements = [sum(counts[:i]) for i in range(size)]

    print(f"\n--- Início do Processamento Paralelo ---")
    print(f"Total de processos: {size}")
    print(f"Total de elementos: {total_elements}")
    start_time = time.time()

    local_data = np.empty(counts[0], dtype=data.dtype)

else:
    data = None
    counts = None
    displacements = None
    total_elements = None

counts = comm.bcast(counts, root=0)
displacements = comm.bcast(displacements, root=0)
total_elements = comm.bcast(total_elements, root=0)

local_count = counts[rank]

if rank != 0:
    local_data = np.empty(local_count, dtype=np.int64)

comm.Scatterv([data, counts, displacements, MPI.LONG], local_data, root=0)

local_perfect_count = contarPerfeitos(local_data)

local_perfect_count64 = np.int64(local_perfect_count)
total_perfect_count = comm.reduce(local_perfect_count64, op=MPI.SUM, root=0)

if rank == 0:
    print(f"Total de números perfeitos no arquivo: {total_perfect_count}")
    print(f"--- Fim do Processamento Paralelo ---\n")
