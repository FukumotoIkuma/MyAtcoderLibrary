"""
N頂点M辺のグラフにおいて、edgeのweightが非負であるもの。
0-1BFSはこれの一部とも言える。
特徴はキューが優先度付きキューとなっており、distanceが最も小さいものから順に処理することである。
"""

from heapq import heapify, heappop, heappush


INF = float("inf")


# N頂点M辺(A[i]-(W[i])->B[i])の有向グラフにおいて、S->Tへ移動する場合
# O(N + Mlog(M+1))
def solve(N: int, M: int, S: int, T: int, A: list[int], B: list[int], W: list[int]):

    # グラフの頂点に辺を追加する
    G: list[list[tuple[int, int]]] = [[] for _ in range(N + 1)]  # Graph
    for a, w, b in zip(A, W, B):
        G[a].append((w, b))

    # vertexまでの最善距離を管理する配列
    dist = [INF] * (N + 1)  # distance
    dist[S] = 0

    # Dijkstra
    que = [(0, S)]
    heapify(que)
    while que:
        d, v = heappop(que)

        # 記録されている最善の距離と追加された時点の距離が異なれば探索しない
        if dist[v] != d:
            continue

        # 最善のコストでゴールに到達したので終了
        if v == T:
            print(d)
            return

        # 次のvertex をキューに追加
        for w, nv in G[v]:
            nd = d + w

            # 処理によりコストが改善しない場合は追加しない
            if dist[nv] <= nd:
                continue

            dist[nv] = nd
            heappush(que, (nd, nv))

    print(-1)
