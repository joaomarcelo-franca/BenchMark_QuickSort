// 4) Quicksort com OpenMP em C
//
// Estratégia: o vetor é dividido em NUM_THREADS partes, cada thread ordena a sua
// parte com quicksort e, no final, as partes ordenadas são intercaladas (merge).
//
// Compilar:  gcc -O2 -fopenmp quicksort_openmp.c -o quicksort_openmp
// Executar:  ./quicksort_openmp

#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define ARQUIVO "../numeros.txt"

// >>>>>>>>>> ALTERE AQUI O NÚMERO DE THREADS (1, 2, 4, 8 ...) <<<<<<<<<<
#define NUM_THREADS 1

void quicksort(int *v, int inicio, int fim) {
    // Ordena v[inicio..fim] no próprio lugar (in-place)
    if (inicio >= fim)
        return;
    int pivo = v[(inicio + fim) / 2];
    int i = inicio, j = fim;
    while (i <= j) {
        while (v[i] < pivo) i++;
        while (v[j] > pivo) j--;
        if (i <= j) {
            int temp = v[i];
            v[i] = v[j];
            v[j] = temp;
            i++;
            j--;
        }
    }
    quicksort(v, inicio, j);
    quicksort(v, i, fim);
}

int *ler_numeros(int *quantidade) {
    FILE *arquivo = fopen(ARQUIVO, "r");
    if (!arquivo) {
        printf("Erro ao abrir %s\n", ARQUIVO);
        exit(1);
    }
    int capacidade = 1024, n = 0, valor;
    int *v = malloc(capacidade * sizeof(int));
    while (fscanf(arquivo, "%d%*[, \n\r\t]", &valor) == 1) {
        if (n == capacidade) {
            capacidade *= 2;
            v = realloc(v, capacidade * sizeof(int));
        }
        v[n++] = valor;
    }
    fclose(arquivo);
    *quantidade = n;
    return v;
}

int main() {
    int n;
    int *v = ler_numeros(&n);
    int *ordenado = malloc(n * sizeof(int));
    int inicios[NUM_THREADS], fins[NUM_THREADS], posicao[NUM_THREADS];
    int tamanho = n / NUM_THREADS;

    printf("Quantidade de numeros: %d\n", n);
    printf("Quantidade de Threads: %d\n", NUM_THREADS);

    for (int t = 0; t < NUM_THREADS; t++) {
        inicios[t] = t * tamanho;
        fins[t] = (t == NUM_THREADS - 1) ? n - 1 : inicios[t] + tamanho - 1;
    }

    double inicio = omp_get_wtime();

    omp_set_num_threads(NUM_THREADS);
    // Cada iteração (uma parte do vetor) é executada por uma thread diferente
    #pragma omp parallel for
    for (int t = 0; t < NUM_THREADS; t++) {
        quicksort(v, inicios[t], fins[t]);
    }

    // Intercala as partes já ordenadas: a cada passo pega o menor entre as partes
    for (int t = 0; t < NUM_THREADS; t++)
        posicao[t] = inicios[t];
    for (int k = 0; k < n; k++) {
        int menor = -1;
        for (int t = 0; t < NUM_THREADS; t++) {
            if (posicao[t] <= fins[t] &&
                (menor == -1 || v[posicao[t]] < v[posicao[menor]]))
                menor = t;
        }
        ordenado[k] = v[posicao[menor]++];
    }

    double fim = omp_get_wtime();

    int correto = 1;
    for (int k = 1; k < n; k++) {
        if (ordenado[k - 1] > ordenado[k]) {
            correto = 0;
            break;
        }
    }
    printf("Ordenado corretamente: %s\n", correto ? "True" : "False");
    printf("Tempo: %.6f segundos\n", fim - inicio);

    free(v);
    free(ordenado);
    return 0;
}