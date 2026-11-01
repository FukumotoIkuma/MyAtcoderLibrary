"""
無向・重みなし木

- 頂点は0から始まるインデックス（0-indexed）で表される。
- クエリの実行前に、`add_edge` を用いてちょうど n-1 本の辺を追加すること。
- クエリ処理は反復的（非再帰）に行われる。
- 公開されている結果配列や隣接リストを、呼び出し側が変更してはならない。
"""

import dis

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DiameterResult:
    """木の直径"""

    length: int  # 辺の本数
    endpoints: tuple[int, int]  # 直径の端点の組の一つ
    path: list[int]  # endpoints[0] -> endpoints[1] の頂点列
    centers: tuple[int, ...]  # 中央の頂点（一つまたは二つ）


@dataclass(frozen=True, slots=True)
class RootedTreeResult:
    root: int
    parent: list[int]  # parent[root] == -1
    depth: list[int]  # rootからの距離
    order: list[int]  # DFSの先行順（親が子より先）
    subtree_size: list[int]
    tin: list[int]  # 0始まりの先行順における位置
    tout: list[int]  # 排他的終端; 部分木 = order[tin[v]:tout[v]]


class Tree:
    def __init__(self, n: int):
        if n < 1:
            raise ValueError("n must be positive")
        self.n = n
        self.G: list[list[int]] = [[] for _ in range(n)]
        self.edge_count = 0

        self._diameter_cache: DiameterResult | None = None
        self._ecc_cache: list[int] | None = None
        self._rooted_cache: RootedTreeResult | None = None
        self._up: list[list[int]] | None = None  # up[j][v] = vの2**j個上の祖先

    def add_edge(self, u: int, v: int) -> None:
        """構築中の木に辺を追加する。閉路ができる場合はValueErrorを送出する。"""
        self._check_vertex(u)
        self._check_vertex(v)

        self.G[u].append(v)
        self.G[v].append(u)
        self.edge_count += 1

        self._diameter_cache = None
        self._ecc_cache = None
        self._rooted_cache = None
        self._up = None

    def diameter(self) -> DiameterResult:
        """経路と中央の頂点を含む直径の一つを返す。初回はO(n)。"""
        self._check_ready()
        if self._diameter_cache is None:
            dist0, _ = self._search(0)
            a = max(range(self.n), key=dist0.__getitem__)
            dist_a, parent_a = self._search(a)
            b = max(range(self.n), key=dist_a.__getitem__)
            length = dist_a[b]

            path = []
            cur = b
            while cur != -1:
                path.append(cur)
                if cur == a:
                    break
                cur = parent_a[cur]
            path.reverse()

            mid = length // 2
            centers = (path[mid],) if length % 2 == 0 else (path[mid], path[mid + 1])
            self._diameter_cache = DiameterResult(length, (a, b), path, centers)
        return self._diameter_cache

    def centers(self) -> tuple[int, ...]:
        """木の中心を返す。直径が偶数なら一つ、奇数なら二つ。初回はO(n)。"""
        return self.diameter().centers

    def distances_from(self, start: int) -> list[int]:
        """startから各頂点までの距離（辺の本数）を返す。O(n)。"""
        self._check_ready()
        self._check_vertex(start)
        return self._search(start)[0]

    def farthest(self, start: int) -> tuple[int, int]:
        """（最遠頂点の一つ、距離）を返す。O(n)。"""
        self._check_ready()
        self._check_vertex(start)
        dist, _ = self._search(start)
        v = max(range(self.n), key=lambda x: dist[x])
        return v, dist[v]

    def eccentricities(self) -> list[int]:
        """各頂点から最遠頂点までの距離を返す。初回はO(n)。"""
        self._check_ready()
        if self._ecc_cache is None:
            a, b = self.diameter().endpoints
            da, _ = self._search(a)
            db, _ = self._search(b)
            self._ecc_cache = [max(x, y) for x, y in zip(da, db)]
        return self._ecc_cache.copy()

    def rooted(self, root: int = 0) -> RootedTreeResult:
        """木を根付きにし、DFS順、親、深さ、部分木、Euler区間を生成する。

        vの部分木はorder[tin[v]:tout[v]]を占める。新しい根ごとにO(n)。
        """
        self._check_ready()
        self._check_vertex(root)
        if self._rooted_cache is not None and self._rooted_cache.root == root:
            return self._rooted_cache

        parent = [-1] * self.n
        depth = [0] * self.n
        order: list[int] = []
        stack = [root]
        while stack:
            v = stack.pop()
            order.append(v)
            for nv in self.G[v]:
                if nv == parent[v]:
                    continue
                parent[nv] = v
                depth[nv] = depth[v] + 1
                stack.append(nv)

        size = [1] * self.n
        for v in reversed(order):
            p = parent[v]
            if p != -1:
                size[p] += size[v]

        tin = [0] * self.n
        for i, v in enumerate(order):
            tin[v] = i
        tout = [tin[v] + size[v] for v in range(self.n)]

        info = RootedTreeResult(root, parent, depth, order, size, tin, tout)
        self._rooted_cache = info
        self._up = None  # 二分累乗法の表は一つの根に対応する
        return info

    def kth_ancestor(self, v: int, k: int, root: int = 0) -> int:
        """根に向かってk本上の祖先を返す。存在しない場合は-1。前処理後はO(log n)。"""
        self._check_vertex(v)
        if k < 0:
            raise ValueError("k must be nonnegative")
        info, up = self._lifting(root)
        if k > info.depth[v]:
            return -1
        bit = 0
        while k:
            if k & 1:
                v = up[bit][v]
            k >>= 1
            bit += 1
        return v

    def is_ancestor(self, u: int, v: int, root: int = 0) -> bool:
        """uがvの祖先か（u == vも含む）を返す。根付き化後はO(1)。"""
        self._check_vertex(u)
        self._check_vertex(v)
        info = self.rooted(root)
        return info.tin[u] <= info.tin[v] < info.tout[u]

    def lca(self, u: int, v: int, root: int = 0) -> int:
        """指定した根付き木における最小共通祖先を返す。O(log n)。"""
        self._check_vertex(u)
        self._check_vertex(v)
        info, up = self._lifting(root)
        if info.depth[u] < info.depth[v]:
            u, v = v, u

        diff = info.depth[u] - info.depth[v]
        bit = 0
        while diff:
            if diff & 1:
                u = up[bit][u]
            diff >>= 1
            bit += 1
        if u == v:
            return u

        for j in range(len(up) - 1, -1, -1):
            if up[j][u] != up[j][v]:
                u = up[j][u]
                v = up[j][v]
        return up[0][u]

    def distance(self, u: int, v: int) -> int:
        """任意の二頂点間の距離を返す。LCAの前処理後はO(log n)。"""
        w = self.lca(u, v)
        info = self.rooted(0)
        return info.depth[u] + info.depth[v] - 2 * info.depth[w]

    def path_between(self, u: int, v: int, root: int = 0) -> list[int]:
        """u -> vの頂点列を返す。O(log n + 経路上の頂点数)。"""
        w = self.lca(u, v, root)
        p = self.rooted(root).parent
        left, right = [], []
        x = u
        while x != w:
            left.append(x)
            x = p[x]
        left.append(w)
        x = v
        while x != w:
            right.append(x)
            x = p[x]
        return left + right[::-1]

    def centroid(self) -> tuple[int, ...]:
        """木の重心を返す。削除後の各連結成分の大きさがn/2以下になる頂点。O(n)。"""
        info = self.rooted(0)
        s, parent = info.subtree_size, info.parent
        ans = []
        for v in range(self.n):
            biggest = self.n - s[v]  # vの親を含む連結成分
            for nv in self.G[v]:
                if nv != parent[v] and s[nv] > biggest:
                    biggest = s[nv]
            if biggest * 2 <= self.n:
                ans.append(v)
        return tuple(ans)

    def _check_vertex(self, v: int) -> None:
        if not 0 <= v < self.n:
            raise IndexError(f"vertex out of range: {v}")

    def _check_ready(self) -> None:
        if self.edge_count != self.n - 1:
            raise ValueError("add exactly n-1 edges before querying the tree")

    def _search(self, start: int) -> tuple[list[int], list[int]]:
        """反復DFSで（startを根とした距離、各頂点の親）を返す。木が完成している必要がある。"""
        dist = [-1] * self.n
        parent = [-1] * self.n
        dist[start] = 0
        stack = [start]
        while stack:
            v = stack.pop()
            for nv in self.G[v]:
                if nv == parent[v]:
                    continue
                parent[nv] = v
                dist[nv] = dist[v] + 1
                stack.append(nv)
        return dist, parent

    def _lifting(self, root: int) -> tuple[RootedTreeResult, list[list[int]]]:
        info = self.rooted(root)
        if self._up is None:
            base = [root if p == -1 else p for p in info.parent]
            up = [base]
            for _ in range(1, self.n.bit_length()):
                prev = up[-1]
                up.append([prev[prev[v]] for v in range(self.n)])
            self._up = up
        return info, self._up


if __name__ == "__main__":
    t = Tree(6)
    for u, v in [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5)]:
        t.add_edge(u, v)

    d = t.diameter()
    print("diameter:", d.length, d.endpoints, d.path, d.centers)
    print("distance(3, 5):", t.distance(3, 5))
    print("lca(3, 4):", t.lca(3, 4))
    print("kth_ancestor(3, 2):", t.kth_ancestor(3, 2))
    print("eccentricities:", t.eccentricities())
    print("centroid(s):", t.centroid())
