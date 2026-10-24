"""
N頂点M辺のグラフにおいて、edgeのweightが0または1であるもの。
weight0の移動をキューの左側に追加することで、同じdistanceであるものを先に処理することができる。
weight1の移動は通常のBFS同様に右側に追加する。
単純なBFSと比較した場合、同じvertexが複数回キューに追加される可能性がある
(1-(weight 1)->2-(weight 1)->4, 1-(weight 1)->3->(weight 0)->4の場合など。2の後に3を訪れる)
すなわち、vertexを訪れたこととが最小のdistanceが確定したことを意味しない。
最小のdistanceが確定したのはキューからそのvertexを取り出したときである。
"""

from collections import deque


INF = float("inf")


# https://atcoder.jp/contests/abc481/tasks/abc481_d
# N頂点M辺(A[i]->B[i])の有向グラフにおいて、S->Tへ移動する場合
def solve(N: int, M: int, S: int, T: int, A: list[int], B: list[int]):
    # weight = 0となる移動も特定する
    mn_next = [INF] * (N + 1)
    for a, b in zip(A, B):
        mn_next[a] = min(mn_next[a], b)

    # グラフの頂点に辺を追加する
    G: list[list[tuple[int, int]]] = [[] for _ in range(N + 1)]  # Graph
    for a, b in zip(A, B):
        w = mn_next[a] != b
        G[a].append((w, b))

    # vertexまでの最善距離を管理する配列
    dist = [INF] * (N + 1)  # distance
    dist[S] = 0

    # 0-1 BFS
    que = deque([(0, S)])
    while que:
        d, v = que.popleft()

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
            if w == 0:
                que.appendleft((nd, nv))
            else:
                que.append((nd, nv))
    print(-1)
