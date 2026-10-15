# 3) Quicksort com MULTIPROCESSING em Python
#
# Estratégia: a lista é dividida em NUM_PROCESSOS partes, cada processo ordena a
# sua parte com quicksort e, no final, as partes ordenadas são intercaladas (merge).

import time, os, heapq
from multiprocessing import Pool

ARQUIVO = "../numeros.txt"

# >>>>>>>>>> ALTERE AQUI O NÚMERO DE PROCESSOS (1, 2, 4, 8 ...) <<<<<<<<<<
NUM_PROCESSOS = 8


def ler_numeros():
    with open(ARQUIVO) as arquivo:
        return [int(x) for x in arquivo.read().replace(",", " ").split()]


def quicksort(lista, inicio, fim):
    # Ordena lista[inicio..fim] no próprio lugar (in-place)
    if inicio >= fim:
        return
    pivo = lista[(inicio + fim) // 2]
    i, j = inicio, fim
    while i <= j:
        while lista[i] < pivo:
            i += 1
        while lista[j] > pivo:
            j -= 1
        if i <= j:
            lista[i], lista[j] = lista[j], lista[i]
            i += 1
            j -= 1
    quicksort(lista, inicio, j)
    quicksort(lista, i, fim)


def ordenar_parte(parte):
    quicksort(parte, 0, len(parte) - 1)
    return parte  # o Pool devolve a parte ordenada para o processo principal


def criar_partes(numeros):
    tamanho = len(numeros) // NUM_PROCESSOS
    partes = []
    for i in range(NUM_PROCESSOS):
        inicio = i * tamanho
        if i == NUM_PROCESSOS - 1:
            fim = len(numeros)
        else:
            fim = inicio + tamanho
        partes.append(numeros[inicio:fim])
    return partes


if __name__ == "__main__":
    print("CPUs disponíveis:", os.cpu_count())
    print("Num. processos:", NUM_PROCESSOS)

    numeros = ler_numeros()
    print(f"Quantidade de números: {len(numeros):,}".replace(",", "."))

    inicio_tempo = time.perf_counter()
    partes = criar_partes(numeros)
    with Pool(NUM_PROCESSOS) as pool:
        resultados = pool.map(ordenar_parte, partes)
    # Intercala as partes já ordenadas em uma única lista ordenada
    ordenada = list(heapq.merge(*resultados))
    fim_tempo = time.perf_counter()

    print(f"Ordenado corretamente: {ordenada == sorted(numeros)}")
    print(f"Tempo: {fim_tempo - inicio_tempo:.4f} segundos")