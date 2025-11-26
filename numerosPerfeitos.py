import numpy as np
from mpi4py import MPI
import math

def eh_perfeito(n):
    if n < 2:
        return False
    soma = 1
    raiz = int(math.sqrt(n))
    for d in range(2, raiz + 1):
        if n % d == 0:
            soma += d
            outro = n // d
            if outro != d:
                soma += outro
    return soma == n

def contar_perfeitos(v):
    qtd = 0
    for i in v:
        if eh_perfeito(i):
            qtd += 1
    return qtd

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    n_proc = comm.Get_size()

    arquivo = 'T.npy'

    if rank == 0:
        dados = np.load(arquivo)
        total = len(dados)

        base = total // n_proc
        sobra = total % n_proc

        tamanhos = []
        for i in range(n_proc):
            if i < sobra:
                tamanhos.append(base + 1)
            else:
                tamanhos.append(base)

        inicios = [0]
        for i in range(1, n_proc):
            inicios.append(inicios[i - 1] + tamanhos[i - 1])

        dados_local = np.empty(tamanhos[0], dtype=dados.dtype)
        
    else:
        dados = None
        tamanhos = None
        inicios = None
        total = None

    tamanhos = MPI.COMM_WORLD.bcast(tamanhos, root=0)
    inicios = MPI.COMM_WORLD.bcast(inicios, root=0)
    total = MPI.COMM_WORLD.bcast(total, root=0)

    tam_local = tamanhos[rank]

    if rank != 0:
        dados_local = np.empty(tam_local, dtype=np.int64)

    comm.Scatterv([dados, tamanhos, inicios, MPI.LONG], dados_local, root=0)

    cont_local = contar_perfeitos(dados_local)
    
    contagem_total = comm.reduce(cont_local, op=MPI.SUM, root=0)

    if rank == 0:
        print("Total de números perfeitos no arquivo:", contagem_total)

if __name__ == "__main__":
    main()
