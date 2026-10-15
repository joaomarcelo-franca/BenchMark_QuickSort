# Executa as duas versões uma vez e monta a tabela comparativa

import sequencial
import concorrente

print("\n===== SEQUENCIAL =====")
tempo_seq = sequencial.executar()

print("\n===== CONCORRENTE =====")
tempo_conc = concorrente.executar()

speedup = tempo_seq / tempo_conc
 
print("\n+-----------------------+-----------+")
print(f"| {'Versão':<21} | {'Tempo (s)':>9} |")
print("+-----------------------+-----------+")
print(f"| {'Sequencial':<21} | {tempo_seq:>9.2f} |")
print(f"| {'Concorrente (asyncio)':<21} | {tempo_conc:>9.2f} |")
print("+-----------------------+-----------+")
print(f"| {'Speedup':<21} | {speedup:>8.2f}x |")
print("+-----------------------+-----------+")


