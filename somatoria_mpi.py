# ---
# Arquivo: A.py
# Aluna: Allicia Rocha dos Santos
# MPI – Somatória Quadrática
# ---

from mpi4py import MPI
import numpy as np

# -----------------------------
# Função para somatória parcial
# -----------------------------
def somatoria_quadratica_parcial(parte):
    soma = 0
    for n in parte:
        n = int(n)
        if n % 2 == 0:     # par → soma
            soma += n * n
        else:              # ímpar → subtrai
            soma -= n * n
    return soma


# -----------------------------
# Inicialização MPI
# -----------------------------
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# -----------------------------
# Processo 0 lê os dados
# -----------------------------
A = np.load("A.npy")
# A = [1,2,3,4,5,6]


# Distribuir o vetor para todos
A = comm.bcast(A, root=0)

# -----------------------------
# Divisão entre os processos
# -----------------------------
chunk = np.array_split(A, size)[rank]

# -----------------------------
# Computar somatória parcial
# -----------------------------
local_sum = somatoria_quadratica_parcial(chunk)

# -----------------------------
# Reduzir resultados (somatório)
# -----------------------------
total_sum = comm.reduce(local_sum, op=MPI.SUM, root=0)

# -----------------------------
# Processo 0 imprime o resultado
# -----------------------------
if rank == 0:
    print(total_sum)

