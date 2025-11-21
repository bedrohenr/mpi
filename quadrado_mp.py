################################################

### Aluno(a): Pedro Henrique Fonseca Ferreira

### Exercício: Grupo AF b

### Conjunto de Dados: P

### Linguagem usada? Python

#################################################

'''
    1. Dado um vetor (conjunto de Dados C)  de inteiros. Desenvolver um programa paralelo que encontre todos os números quadrados perfeitos (Ex. 25,4,144) com speedup maior que1. ( referência de tempo sequencial=  1,9002347)
    2. retorno(Print no console, numérico):  quantidade  de quadrados perfeitos
'''

import math
import numpy as np
import multiprocessing as mp
import time # Importado para calcular o speedup

# --- 1. FUNÇÃO DE VERIFICAÇÃO DE QUADRADO PERFEITO (Lógica Interna) ---

def isQuadradoPerfeito(num):
    """
    Verifica se um número é um quadrado perfeito de forma eficiente.
    """
    if num < 0:
        return False
    # Evita math.isqrt para 0 e 1, que são triviais e seguros
    if num == 0 or num == 1:
        return True 

    # math.isqrt() para raiz quadrada inteira.
    raiz = math.isqrt(num)

    return raiz * raiz == num

# --- 2. FUNÇÃO SEQUENCIAL (TAREFA DO PROCESSO) RECEBENDO O CHUNK ---

def seq_split(bloco):
    """
    Função executada por cada processo.
    Recebe uma fatia (chunk) do vetor e conta os quadrados perfeitos.

    Args:
        bloco (np.ndarray): Uma fatia do vetor original.

    Returns:
        int: O número de quadrados perfeitos encontrados no bloco.
    """
    # Renomeando a variável para ser semanticamente correta (não são 'primos')
    quadrados_encontrados = 0 
    
    for numero in bloco:
        # Chama a função de verificação. A conversão para int(numero) é 
        # opcional, mas garante que o tipo Python nativo seja passado, se necessário.
        if isQuadradoPerfeito(int(numero)): 
            quadrados_encontrados += 1
            
    return quadrados_encontrados

# --- 3. FUNÇÃO PARALELA (COORDENADOR) USANDO np.array_split ---

def paralel(vetor, processos=None):
    """
    Coordena a contagem de quadrados perfeitos particionando o vetor
    com numpy.array_split e usa pool.map para paralelizar.
    """
    N = len(vetor)
    
    if processos is None:
        processos = mp.cpu_count()
        
    if processos > N:
        processos = N

    # 3.1. Particionamento do Vetor usando np.array_split
    # Esta função divide o vetor em 'processos' blocos de forma eficiente.
    blocos = np.array_split(vetor, processos)
    
    contagem_total = 0 
    
    with mp.Pool(processes=processos) as pool:
        
        # pool.map distribui cada bloco da lista 'blocos' para a função seq_split.
        contagens_locais = pool.map(seq_split, blocos)

        # 3.2. Combinação dos Resultados
        contagem_total = sum(contagens_locais)
            
    return contagem_total 

# --- EXECUÇÃO PRINCIPAL E CÁLCULO DE SPEEDUP ---

if __name__ == '__main__':
    
    PROCESSOS = 8

    LISTA = np.load('P.npy')
    
    print(paralel(LISTA, PROCESSOS))
