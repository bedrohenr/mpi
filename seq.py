import numpy as np
import math
import sys

# Assume 'your_file.npy' is the name of your NPY file
file_path = 'P.npy'

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
    # Só precisamos verificar divisores até a raiz quadrada de n
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

if __name__ == "__main__":
    # Load the NPY file
    data = np.load(file_path)

    count = 0
    # Print the full array
    for num in data:
        if(is_prime(num)):
            count += 1

    print(count)
