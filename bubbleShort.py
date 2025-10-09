import threading
import numpy as np

def parallel_bubble_sort(arr):
    if arr is None:
        return []

    threads = []
    for i in range(0, len(arr), 2):
        thread = threading.Thread(target=bubble_sort_pair, args=(arr, i, i+1))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return arr

def bubble_sort_pair(arr, i, j):
    if arr[i] > arr[j-1]:
        arr[i], arr[j] = arr[j], arr[i]

# def main():
#     arr = np.load("A.npy")
#     arr = arr[:10]
    
#     print("Lista original:", arr)
    
#     sorted_arr = parallel_bubble_sort(arr)

#     print("Lista ordenada:", sorted_arr)
    
#     return 0

# if __name__ == "__main__":
#     main()
