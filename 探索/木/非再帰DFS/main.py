"""
木の探索においてDFS/BFSを主に使いたいが、木の探索においてはその性質上探索中に戻り値を用いたい場合がほとんどである
python(特にpypy)では再帰関数が非常に低速のため、再帰関数を用いずに戻り値を受け取ることが理想的である
"""

from collections import deque

N = 100
G: list[list[int]] = [[] for _ in range(N)]

parent = [-1] * N
parent[0] = 0
order = []
que = deque([0])

while que:
    v = que.pop()  # DFS
    order.append(v)

    for nv in G[v]:
        if nv == parent[v]:
            continue
        parent[nv] = v
        que.append(nv)

# 戻りがけ：子から親へ
dp = [0] * N
for v in reversed(order):
    for nv in G[v]:
        if nv == parent[v]:  # 親方向への辺は除外
            continue
        # dp[nv] を使って dp[v] を更新
