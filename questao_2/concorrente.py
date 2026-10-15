# Versão CONCORRENTE com asyncio - processamento de pedidos (IO-bound simulado)
# Cada consulta simula uma espera de I/O com asyncio.sleep, liberando o Event Loop

import asyncio
import time

PEDIDOS = ["Pedido 1", "Pedido 2", "Pedido 3", "Pedido 4", "Pedido 5"]


async def consultar_cliente(pedido):
    print(f"[{pedido}] Consultando cliente...")
    await asyncio.sleep(1)  # suspende a coroutine; o Event Loop executa outras tarefas
    print(f"[{pedido}] Cliente encontrado")
    return "Cliente 123"


async def consultar_produtos(pedido):
    print(f"[{pedido}] Consultando produtos...")
    await asyncio.sleep(1)
    print(f"[{pedido}] Produtos encontrados")
    return ["Produto A", "Produto B"]


async def consultar_pagamento(pedido):
    print(f"[{pedido}] Consultando pagamento...")
    await asyncio.sleep(2)
    print(f"[{pedido}] Pagamento aprovado")
    return "Aprovado"


async def processar_pedido(pedido):
    # As 3 consultas do mesmo pedido rodam de forma concorrente
    cliente, produtos, pagamento = await asyncio.gather(
        consultar_cliente(pedido),
        consultar_produtos(pedido),
        consultar_pagamento(pedido),
    )
    return pedido, cliente, produtos, pagamento


async def main():
    # Todos os pedidos também são processados de forma concorrente
    return await asyncio.gather(*(processar_pedido(p) for p in PEDIDOS))


def executar():
    inicio = time.perf_counter()
    resultados = asyncio.run(main())
    fim = time.perf_counter()
    print()
    for r in resultados:
        print(r)
    return fim - inicio


if __name__ == "__main__":
    tempo = executar()
    print(f"\nTempo total (concorrente): {tempo:.2f} segundos")
