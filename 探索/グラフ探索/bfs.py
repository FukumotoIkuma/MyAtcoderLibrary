"""
N頂点M辺のグラフにおいて、edgeのweightが1（一定)であるもの。
"""

from collections import deque

INF = float("inf")


# N頂点M辺(A[i]->B[i])の有向グラフにおいて、S->Tへ移動する場合
def solve(N: int, M: int, S: int, T: int, A: list[int], B: list[int]):

    # グラフの頂点に辺を追加する
    G: list[list[tuple[int, int]]] = [[] for _ in range(N + 1)]  # Graph
    for a, b in zip(A, B):
        # weightが一定のためココで追加する絶対的必要性はない
        # 0-1 bfsやダイクストラ法の理解で便利なため統一して処理する
        G[a].append((1, b))

    # vertexまでの最善距離を管理する配列
    dist = [INF] * (N + 1)  # distance
    dist[S] = 0

    # BFS
    que = deque([(0, S)])
    while que:
        d, v = que.popleft()

        # 確定済みではないdistanceがキューに入ることは無い

        # 最善のコストでゴールに到達したので終了
        if v == T:
            print(d)
            return

        # 次のvertex をキューに追加
        for w, nv in G[v]:
            nd = d + w

            # 処理によりコストが改善しない場合は追加しない
            # BFSではdistが確定した時点で改善する可能性はないので、到達=distance確定である
            if dist[nv] != INF:
                continue

            dist[nv] = nd
            que.append((nd, nv))
    print(-1)
