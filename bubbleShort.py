import threading
import numpy as np

def bubble_sort_pair(arr, i): 
    j = i + 1
    if j < len(arr) and arr[i] > arr[j]:
        arr[i], arr[j] = arr[j], arr[i]

def parallel_bubble_sort(arr):
    N = len(arr)
    if N <= 1:
        return arr

    # A ordenação completa requer N iterações (passes)
    for _ in range(N):
        # 1. Fase Ímpar (Compara: (1, 2), (3, 4), (5, 6), ...)
        threads_odd = []
        for i in range(1, N, 2):
            thread = threading.Thread(target=bubble_sort_pair, args=(arr, i))
            threads_odd.append(thread)
            thread.start()
        
        # Espera todas as trocas da Fase Ímpar terminarem
        for thread in threads_odd:
            thread.join()

        # 2. Fase Par (Compara: (0, 1), (2, 3), (4, 5), ...)
        threads_even = []
        for i in range(0, N, 2):
            thread = threading.Thread(target=bubble_sort_pair, args=(arr, i))
            threads_even.append(thread)
            thread.start()

        # Espera todas as trocas da Fase Par terminarem
        for thread in threads_even:
            thread.join()

    return arr

def main():
    # arr = np.load("A.npy")
    # arr = arr[:10000]
    arr = np.arange(1000, 0, -1, dtype='i')  # Integer array: [0, 1, 2, ..., 15]
    
    print("Lista original:", arr)
    sorted_arr = parallel_bubble_sort(arr)
    print("Lista ordenada:", sorted_arr)
    return 0

if __name__ == "__main__":
    main()
