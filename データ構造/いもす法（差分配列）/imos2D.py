class Imos2D:
    """二次元いもす法。長方形への一括加算。"""

    def __init__(self, H: int, W: int):
        self.H = H
        self.W = W
        self.diff = [[0] * (W + 1) for _ in range(H + 1)]
        self.built = False

    def add(self, left, right, value: int = 1):
        """[y1, y2) × [x1, x2) にvalueを加算"""
        if self.built:
            raise RuntimeError("build() 後は add() できません")

        y1, x1 = left
        y2, x2 = right
        D = self.diff

        D[y1][x1] += value
        D[y1][x2] -= value
        D[y2][x1] -= value
        D[y2][x2] += value

    def build(self):
        """縦横の累積和を取って復元"""
        if self.built:
            return

        D = self.diff
        H, W = self.H, self.W

        for y in range(H):
            row = D[y]
            for x in range(1, W):
                row[x] += row[x - 1]

        for y in range(1, H):
            row = D[y]
            prev = D[y - 1]
            for x in range(W):
                row[x] += prev[x]

        self.built = True

    def get(self, pos):
        """build() 後に指定座標の値を取得"""
        if not self.built:
            raise RuntimeError("先に build() を実行してください")

        y, x = pos
        return self.diff[y][x]


if __name__ == "__main__":
    imos = Imos2D(4, 5)

    imos.add((1, 1), (3, 4), 2)
    imos.add((2, 2), (4, 5), 3)

    imos.build()

    print(imos.get((1, 1)))  # 2
    print(imos.get((2, 2)))  # 5
    print(imos.get((3, 4)))  # 3
