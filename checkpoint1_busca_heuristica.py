"""
Checkpoint 1 — Busca Heurística em Grafos
Engenharia de Software — IA & Machine Learning
Algoritmo: A* (A-estrela)
Problema: encontrar o caminho de A (PortalWeb) até R (BancoDeDados)
"""

import heapq
import datetime

# ─────────────────────────────────────────────
# ETAPA A — Modelagem do problema
# ─────────────────────────────────────────────

# Grafo extraído da Figura 1 (arestas bidirecionais com pesos)
grafo = {
    'A': {'B': 73, 'C': 64, 'D': 89, 'E': 104},
    'B': {'A': 73, 'H': 83},
    'C': {'A': 64, 'I': 64},
    'D': {'A': 89, 'N': 89, 'J': 40},     # D-J via E-J confirmado pelo layout
    'E': {'A': 104, 'J': 40},
    'F': {'I': 31, 'M': 84},
    'G': {'J': 35, 'Q': 113},
    'H': {'B': 83, 'K': 35, 'L': 36},
    'I': {'C': 64, 'F': 31, 'L': 28, 'M': 20},
    'J': {'D': 40, 'E': 40, 'G': 35, 'N': 53, 'Q': 80},
    'K': {'H': 35, 'P': 63},
    'L': {'H': 36, 'I': 28, 'O': 41},
    'M': {'F': 84, 'I': 20, 'O': 50},
    'N': {'D': 89, 'J': 53, 'R': 65},
    'O': {'L': 41, 'M': 50, 'P': 41, 'R': 72},
    'P': {'K': 63, 'O': 41, 'R': 65, 'Q': 65},   # P-Q inferido do layout
    'Q': {'G': 113, 'J': 80, 'P': 65, 'R': 65},
    'R': {'N': 65, 'O': 72, 'P': 65, 'Q': 65},
}

# Heurística h(n) — estimativa do custo restante até R (fornecida pelo enunciado)
heuristica = {
    'A': 240, 'B': 186, 'C': 182, 'D': 163,
    'E': 170, 'F': 150, 'G': 165, 'H': 139,
    'I': 120, 'J': 130, 'K': 122, 'L': 104,
    'M': 100, 'N':  77, 'O':  72, 'P':  65,
    'Q':  65, 'R':   0,
}

# Legenda contextual dos nós
legenda = {
    'A': 'PortalWeb (entrada do incidente)',
    'R': 'BancoDeDados (correção validada)',
    'B': 'Serviço de Autenticação',
    'C': 'Gateway de APIs',
    'D': 'Fila de Pedidos',
    'E': 'Serviço de Notificações',
    'F': 'Módulo de Cache',
    'G': 'Serviço Externo de Monitoramento',
    'H': 'Serviço de Sessão',
    'I': 'Orquestrador Interno',
    'J': 'Serviço de Pagamentos',
    'K': 'Módulo de Auditoria',
    'L': 'Camada de Negócios',
    'M': 'Microserviço de Dados',
    'N': 'Módulo de Persistência',
    'O': 'Camada de Integração',
    'P': 'Serviço de Relatórios',
    'Q': 'Módulo de Reconciliação',
}


# ─────────────────────────────────────────────
# Implementação do A* com registro de expansão
# ─────────────────────────────────────────────

def a_star(grafo, heuristica, inicio, objetivo):
    """
    Algoritmo A* — f(n) = g(n) + h(n)
    Retorna: (caminho, custo_total, ordem_expansao)
    """
    # fila de prioridade: (f, g, nó, caminho)
    fila = [(heuristica[inicio], 0, inicio, [inicio])]
    visitados = {}           # nó → menor g encontrado
    ordem_expansao = []      # registro da ordem de expansão

    while fila:
        f, g, no_atual, caminho = heapq.heappop(fila)

        # Ignora se já encontramos custo menor para este nó
        if no_atual in visitados and visitados[no_atual] <= g:
            continue

        visitados[no_atual] = g
        ordem_expansao.append((no_atual, g, f))

        if no_atual == objetivo:
            return caminho, g, ordem_expansao

        for vizinho, peso in grafo[no_atual].items():
            novo_g = g + peso
            novo_f = novo_g + heuristica[vizinho]
            if vizinho not in visitados or visitados[vizinho] > novo_g:
                heapq.heappush(fila, (novo_f, novo_g, vizinho, caminho + [vizinho]))

    return None, float('inf'), ordem_expansao


# ─────────────────────────────────────────────
# EXECUÇÃO COM HEURÍSTICA ORIGINAL
# ─────────────────────────────────────────────

print("=" * 60)
print("  CHECKPOINT 1 — BUSCA HEURÍSTICA A* (A-ESTRELA)")
print("  Engenharia de Software — IA & Machine Learning")
print(f"  Executado em: {datetime.datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
print("=" * 60)
print(f"\n  Algoritmo  : A* (A-estrela)  |  f(n) = g(n) + h(n)")
print(f"  Início     : A — PortalWeb (entrada do incidente)")
print(f"  Objetivo   : R — BancoDeDados (correção validada)")
print(f"  Nós no grafo: {len(grafo)}  |  Nós com heurística: {len(heuristica)}")
print("-" * 60)

caminho, custo, expansao = a_star(grafo, heuristica, 'A', 'R')

print("\n📌 ORDEM DE EXPANSÃO DOS NÓS:")
print(f"  {'Nó':<5} {'g(n) — custo acum.':<25} {'f(n) = g+h'}")
print(f"  {'-'*50}")
for no, g, f in expansao:
    print(f"  {no:<5} {g:<25} {f}")

print(f"\n CAMINHO ENCONTRADO: {' → '.join(caminho)}")
print(f" CUSTO TOTAL: {custo}")
print(f" NÓS EXPANDIDOS: {len(expansao)}")

print("\n CAMINHO COM CONTEXTO DE ENGENHARIA DE SOFTWARE:")
for i, no in enumerate(caminho):
    desc = legenda.get(no, no)
    prefixo = " INÍCIO:" if i == 0 else ("🏁 FIM:   " if i == len(caminho)-1 else f"  Passo {i}:")
    print(f"  {prefixo} [{no}] {desc}")

print("\n" + "=" * 60)
print("  *** EVIDÊNCIA DE EXECUÇÃO — RESULTADO FINAL ***")
print("=" * 60)
print(f"  Rota final  : {' → '.join(caminho)}")
print(f"  Custo total : {custo}")
print(f"  Nós visitados: {len(expansao)}")
print(f"  Status      : SOLUÇÃO ENCONTRADA ✔")
print(f"  Executado em: {datetime.datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
print("=" * 60)


# ─────────────────────────────────────────────
# EXECUÇÃO COM h(n) = 0 (Dijkstra / busca de custo uniforme)
# ─────────────────────────────────────────────

heuristica_zero = {no: 0 for no in heuristica}

caminho_z, custo_z, expansao_z = a_star(grafo, heuristica_zero, 'A', 'R')

print("\n" + "=" * 60)
print("  COMPARAÇÃO: h(n) = 0 para todos os nós (Dijkstra)")
print("=" * 60)
print(f"\n CAMINHO ENCONTRADO: {' → '.join(caminho_z)}")
print(f" CUSTO TOTAL: {custo_z}")
print(f" NÓS EXPANDIDOS: {len(expansao_z)}")

print("\n RESUMO COMPARATIVO:")
print(f"  {'Abordagem':<35} {'Nós Expandidos':<20} {'Custo Total'}")
print(f"  {'-'*65}")
print(f"  {'A* com heurística original':<35} {len(expansao):<20} {custo}")
print(f"  {'Dijkstra (h=0)':<35} {len(expansao_z):<20} {custo_z}")