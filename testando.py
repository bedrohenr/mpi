# hello_mpi.py
from mpi4py import MPI
import socket

# Inicializa o MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()  # O rank (ID) do processo atual
size = comm.Get_size()  # O número total de processos
hostname = socket.gethostname() # O hostname da máquina onde o processo está rodando

print(f"Processo {rank}/{size - 1} em: {hostname}")