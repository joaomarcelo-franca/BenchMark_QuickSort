# Versão SEQUENCIAL - processamento de pedidos (IO-bound simulado)
# Cada consulta simula uma espera de I/O (banco de dados / API externa) com time.sleep

import time

PEDIDOS = ["Pedido 1", "Pedido 2", "Pedido 3", "Pedido 4", "Pedido 5"]


def consultar_cliente(pedido):
    print(f"[{pedido}] Consultando cliente...")
    time.sleep(1)  # simula espera de I/O
    print(f"[{pedido}] Cliente encontrado")
    return "Cliente 123"


def consultar_produtos(pedido):
    print(f"[{pedido}] Consultando produtos...")
    time.sleep(1)
    print(f"[{pedido}] Produtos encontrados")
    return ["Produto A", "Produto B"]


def consultar_pagamento(pedido):
    print(f"[{pedido}] Consultando pagamento...")
    time.sleep(2)
    print(f"[{pedido}] Pagamento aprovado")
    return "Aprovado"


def processar_pedido(pedido):
    # Cada consulta só começa quando a anterior termina
    cliente = consultar_cliente(pedido)
    produtos = consultar_produtos(pedido)
    pagamento = consultar_pagamento(pedido)
    return pedido, cliente, produtos, pagamento


def executar():
    inicio = time.perf_counter()
    resultados = [processar_pedido(p) for p in PEDIDOS]
    fim = time.perf_counter()
    print()
    for r in resultados:
        print(r)
    return fim - inicio


if __name__ == "__main__":
    tempo = executar()
    print(f"\nTempo total (sequencial): {tempo:.2f} segundos")
