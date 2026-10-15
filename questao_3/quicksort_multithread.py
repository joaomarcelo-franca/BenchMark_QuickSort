# 2) Quicksort com MULTITHREADING em Python (com e sem GIL)
#
# Estratégia: a lista é dividida em NUM_THREADS partes, cada thread ordena a sua
# parte com quicksort e, no final, as partes ordenadas são intercaladas (merge).
#
# ===================== LIGAR / DESLIGAR O GIL =====================
# O GIL não pode ser ligado/desligado de dentro do código, só na hora de executar.
# É preciso usar o Python free-threaded (python3.13t ou python3.14t):
#
#   COM GIL:  python3 quicksort_threads.py
#   SEM GIL:  python3.14t quicksort_threads.py
#
# (O python3 normal sempre roda COM GIL.)
# A linha "GIL está habilitado" na saída confirma qual modo está ativo.
# ==================================================================

import sys, time, os, threading, heapq

ARQUIVO = "../numeros.txt"

# >>>>>>>>>> ALTERE AQUI O NÚMERO DE THREADS (1, 2, 4, 8 ...) <<<<<<<<<<
NUM_THREADS = 16


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


def ordenar_parte(parte, indice, resultados):
    quicksort(parte, 0, len(parte) - 1)
    resultados[indice] = parte  # cada thread escreve só na sua posição


def criar_partes(numeros):
    tamanho = len(numeros) // NUM_THREADS
    partes = []
    for i in range(NUM_THREADS):
        inicio = i * tamanho
        if i == NUM_THREADS - 1:
            fim = len(numeros)
        else:
            fim = inicio + tamanho
        partes.append(numeros[inicio:fim])
    return partes


if __name__ == "__main__":
    print("Python:", sys.version)
    gil = sys._is_gil_enabled() if hasattr(sys, "_is_gil_enabled") else True
    print("GIL está habilitado:", gil)
    print("CPUs disponíveis:", os.cpu_count())
    print("Num. threads:", NUM_THREADS)

    numeros = ler_numeros()
    print(f"Quantidade de números: {len(numeros):,}".replace(",", "."))

    inicio_tempo = time.perf_counter()
    partes = criar_partes(numeros)
    resultados = [None] * NUM_THREADS
    threads = []
    for i in range(NUM_THREADS):
        thread = threading.Thread(target=ordenar_parte, args=(partes[i], i, resultados))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    # Intercala as partes já ordenadas em uma única lista ordenada
    ordenada = list(heapq.merge(*resultados))
    fim_tempo = time.perf_counter()

    print(f"Ordenado corretamente: {ordenada == sorted(numeros)}")
    print(f"Tempo: {fim_tempo - inicio_tempo:.4f} segundos")