# 1) Quicksort SEQUENCIAL em Python
# Lê os números de numeros.txt, ordena com quicksort e mede o tempo

import time

ARQUIVO = "../numeros.txt"


def ler_numeros():
    with open(ARQUIVO) as arquivo:
        return [int(x) for x in arquivo.read().replace(",", " ").split()]


def quicksort(lista, inicio, fim):
    # Ordena lista[inicio..fim] no próprio lugar (in-place)
    if inicio >= fim:
        return
    pivo = lista[(inicio + fim) // 2]  # pivô no meio evita o pior caso em listas já ordenadas
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


if __name__ == "__main__":
    numeros = ler_numeros()
    print(f"Quantidade de números: {len(numeros):,}".replace(",", "."))

    inicio_tempo = time.perf_counter()
    quicksort(numeros, 0, len(numeros) - 1)
    fim_tempo = time.perf_counter()

    print(f"Ordenado corretamente: {numeros == sorted(numeros)}")
    print(f"Tempo: {fim_tempo - inicio_tempo:.4f} segundos")