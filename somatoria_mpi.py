# --- 
# Aluna: Allicia Rocha dos Santos
# Avaliação 2
# Grupo B
# ---

import numpy as np
import math
from concurrent.futures import ProcessPoolExecutor

# --- Função parcial de Cálculo Quadrático ---
def somatoria_quadratica_parcial(parte):
    soma = 0
    for n in parte:
        n_int = int(n)
        
        if n_int % 2 == 0:
            soma += n ** 2
        else:
            soma -= n ** 2
    return soma

def somatoria_quadratica_paralela(array, num_threads):
    partes = np.array_split(array, num_threads)

    with ProcessPoolExecutor(max_workers=num_threads) as executor:
        resultados = list(executor.map(somatoria_quadratica_parcial, partes))

    return sum(resultados)

if __name__ == '__main__':
    try:
        array = np.load("A.npy", allow_pickle=True)
    except FileNotFoundError:
        print("Erro: O arquivo 'A.npy' não foi encontrado.")
        array = np.array([1, 2, 3, 4, 5, 6], dtype=float)
        print(f"Usando array de exemplo para demonstração: {array}")

    num_threads = 8 

    resultado = somatoria_quadratica_paralela(array, num_threads=num_threads)

    print(f"Somatória quadrática (com {num_threads} threads) = {resultado}")