from itertools import product


class PrefixSumND:
    """N次元累積和。取得範囲は各軸とも半開区間 [left, right)。"""

    def __init__(self, A):
        # 多次元リストの形状を取得
        shape = []
        node = A
        while isinstance(node, (list, tuple)):
            if not node:
                raise ValueError("空の軸は扱えません")
            shape.append(len(node))
            node = node[0]

        if not shape:
            raise ValueError("多次元配列を指定してください")

        self.shape = tuple(shape)
        self.d = len(shape)
        self.size = tuple(n + 1 for n in shape)

        # 多次元座標を1次元インデックスに変換
        self.stride = [1] * self.d
        for i in range(self.d - 2, -1, -1):
            self.stride[i] = self.stride[i + 1] * self.size[i + 1]

        total = self.size[0] * self.stride[0]
        self.data = [0] * total

        # 元配列を平坦化
        values = []

        def flatten(node, depth):
            if depth == self.d:
                if isinstance(node, (list, tuple)):
                    raise ValueError("配列の形状が不揃いです")
                values.append(node)
                return

            if not isinstance(node, (list, tuple)) or len(node) != self.shape[depth]:
                raise ValueError("配列の形状が不揃いです")

            for child in node:
                flatten(child, depth + 1)

        flatten(A, 0)

        # 各軸の先頭に0を追加した位置へ格納
        for pos, value in zip(product(*(range(n) for n in self.shape)), values):
            idx = sum((p + 1) * s for p, s in zip(pos, self.stride))
            self.data[idx] = value

        # 各軸に沿って累積和
        D = self.data
        for step, width in zip(self.stride, self.size):
            block = step * width

            for start in range(0, len(D), block):
                for idx in range(start + step, start + block):
                    D[idx] += D[idx - step]

    def get(self, left, right):
        """超直方体 [left, right) の合計を取得"""
        if len(left) != self.d or len(right) != self.d:
            raise ValueError("座標の次元数が一致しません")
        if any(not 0 <= l <= r <= n for l, r, n in zip(left, right, self.shape)):
            raise ValueError("座標が範囲外です")

        base = sum(r * s for r, s in zip(right, self.stride))
        offsets = [(r - l) * s for l, r, s in zip(left, right, self.stride)]

        ans = 0

        # 2^d 個の頂点を包除原理で足し引き
        for mask in range(1 << self.d):
            idx = base

            for axis in range(self.d):
                if mask >> axis & 1:
                    idx -= offsets[axis]

            if mask.bit_count() & 1:
                ans -= self.data[idx]
            else:
                ans += self.data[idx]

        return ans


if __name__ == "__main__":
    A = [
        [[1, 2], [3, 4]],
        [[5, 6], [7, 8]],
    ]

    S = PrefixSumND(A)

    print(S.get((0, 0, 0), (2, 2, 2)))  # 36
    print(S.get((1, 0, 0), (2, 2, 2)))  # 26
