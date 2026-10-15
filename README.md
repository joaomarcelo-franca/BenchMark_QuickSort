# AT — Linguagens de Programação: Concorrência e Paralelismo

Comparação de desempenho entre implementações sequenciais, concorrentes e paralelas em Python e C, cobrindo um problema **IO-bound** (com `asyncio`) e um problema **CPU-bound** (Quicksort com multithreading, multiprocessing e OpenMP).

## Estrutura

```
AT_LP/
├── ambiente.txt                 # Especificação da máquina usada nos testes
├── numeros.txt                  # 2.000.000 de inteiros usados pelo Quicksort
├── BENCHMARK_QUICKSORT.xlsx     # Tempos, speedup, eficiência e gráficos
├── at.pdf.odt                   # Enunciado e respostas do trabalho
├── questao_2/                   # IO-bound: sequencial x asyncio
│   ├── sequencial.py
│   ├── concorrente.py
│   └── comparativo.py
└── questao_3/                   # CPU-bound: Quicksort
    ├── quicksort_sequencial.py
    ├── quicksort_multithread.py
    ├── quicksort_multiprocessing.py
    ├── quicksort_openMP.c
    └── quicksort_openMP_{1,2,4,8}   # binários compilados com 1, 2, 4 e 8 threads
```

## Ambiente de testes

Todos os testes foram executados na mesma máquina (detalhes em `ambiente.txt`):

| Item | Configuração |
|------|--------------|
| Sistema operacional | Fedora Linux 44 (Workstation), kernel 7.2.7 |
| Virtualização | Nenhuma (máquina física) |
| Máquina | ASUS Vivobook S 14 (S5406SA) |
| CPU | Intel Core Ultra 7 256V — 8 núcleos, 1 thread por núcleo, até 4,8 GHz |
| Memória | 15 GiB RAM + 8 GiB swap (zram) |
| Disco | NVMe 512 GB |

O arquivo foi gerado com:

```bash
{
  echo "=== SISTEMA OPERACIONAL ==="; cat /etc/os-release | grep -E "^(NAME|VERSION)="; echo "Kernel: $(uname -r)"
  echo; echo "=== VIRTUALIZAÇÃO ==="; systemd-detect-virt; hostnamectl | grep -E "Virtualization|Hardware|Chassis"
  echo; echo "=== CPU ==="; lscpu | grep -E "Model name|^CPU\(s\)|Socket|Core|Thread|MHz"
  echo; echo "=== MEMÓRIA ==="; free -h
  echo; echo "=== DISCO ==="; lsblk -d -o NAME,SIZE,TYPE,MODEL
} > ambiente.txt
```

## Questão 2 — Aplicação IO-bound com Asyncio

Simula o processamento de 5 pedidos. Cada pedido faz três consultas que imitam esperas de I/O (banco de dados / API externa):

| Consulta | Espera |
|----------|--------|
| Cliente | 1 s |
| Produtos | 1 s |
| Pagamento | 2 s |

- **`sequencial.py`** — usa `time.sleep`; cada consulta só começa quando a anterior termina. Tempo esperado: 5 × (1 + 1 + 2) ≈ **20 s**.
- **`concorrente.py`** — usa `asyncio.sleep` e `asyncio.gather`; as três consultas de cada pedido e todos os pedidos rodam de forma concorrente no Event Loop. Tempo esperado ≈ **2 s** (a maior espera individual).
- **`comparativo.py`** — executa as duas versões e imprime uma tabela com os tempos e o speedup (≈ 10x).

O ganho vem de o Event Loop aproveitar o tempo ocioso de espera de I/O para avançar outras tarefas, sem precisar de várias threads ou processos.

```bash
cd questao_2
python3 sequencial.py
python3 concorrente.py
python3 comparativo.py
```

## Questão 3 — Aplicação CPU-bound: Quicksort

Ordenação de 2.000.000 de inteiros lidos de `numeros.txt` (complexidade média O(n log n)). As versões paralelas usam a mesma estratégia: dividir o vetor em *N* partes, ordenar cada parte com Quicksort em paralelo e intercalar (merge) as partes ordenadas no final. Todas verificam se o resultado está corretamente ordenado e mostram o tempo de execução.

> Os scripts leem `../numeros.txt`, então devem ser executados de dentro da pasta `questao_3`.

```bash
cd questao_3
```

### 1. Sequencial (Python)

```bash
python3 quicksort_sequencial.py
```

### 2. Multithreading (Python, com e sem GIL)

Altere `NUM_THREADS` no início do arquivo (1, 2, 4, 8, ...). O GIL não pode ser ligado ou desligado pelo código, apenas pelo interpretador utilizado:

```bash
python3 quicksort_multithread.py      # COM GIL (CPython padrão)
python3.14t quicksort_multithread.py  # SEM GIL (CPython free-threaded)
```

A saída mostra `GIL está habilitado: True/False` para confirmar o modo.

### 3. Multiprocessing (Python)

Altere `NUM_PROCESSOS` no início do arquivo (1, 2, 4, 8, ...):

```bash
python3 quicksort_multiprocessing.py
```

### 4. OpenMP (C)

Altere `#define NUM_THREADS` no arquivo (1, 2, 4, 8, ...), compile e execute:

```bash
gcc -O2 -fopenmp quicksort_openMP.c -o quicksort_openMP_8
./quicksort_openMP_8
```

Os binários `quicksort_openMP_1`, `_2`, `_4` e `_8` já estão compilados com o número de threads correspondente.

## Resultados

Os tempos medidos estão em **`BENCHMARK_QUICKSORT.xlsx`**, que calcula automaticamente:

- **Speedup** = T₁ / Tₙ
- **Eficiência** = Speedup / n

onde T₁ é o tempo com 1 thread/processo da mesma implementação. A planilha também traz gráficos comparando cada implementação com o speedup ideal.

## Requisitos

- Python 3.13+ (e, para os testes sem GIL, a build free-threaded `python3.13t` / `python3.14t`)
- GCC com suporte a OpenMP (`libgomp`)
- Nenhuma biblioteca externa — apenas a biblioteca padrão do Python
