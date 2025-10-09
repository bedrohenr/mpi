from mpi4py import MPI
import numpy as np
import bubbleShort

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Total size of the array (must be divisible by number of processes for simplicity)
N = 100 

# Step 1: Create data only on the root process
if rank == 0:
    data = np.arange(N, dtype='i')  # Integer array: [0, 1, 2, ..., 15]
    # data = np.load('A.npy')  # Integer array: [0, 1, 2, ..., 15]
    print("Original array:", data)
else:
    data = None

# Step 2: Scatter data to all processes
local_n = N // size
local_data = np.empty(local_n, dtype='i')

comm.Scatter(data, local_data, root=0)

# Step 3: Each process sorts its part of the array
print("Lista original:", local_data)
sorted_arr = bubbleShort.parallel_bubble_sort(data)
print("Lista ordenada:", sorted_arr)

# atualizando a variavel data com os itens ordenados
local_result = sorted_arr

# Step 4: Gather results at the root process
result = None
if rank == 0:
    result = np.empty(N, dtype='i')

comm.Gather(local_result, result, root=0)

# Step 5: Print result in the root process
if rank == 0:
    print("Resultado:", result)