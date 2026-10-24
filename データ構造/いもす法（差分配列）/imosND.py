class ImosND:
    """N次元いもす法。各軸の更新区間は半開区間 [left, right)。"""

    def __init__(self, shape):
        self.shape = tuple(shape)
        self.d = len(shape)

        # 各軸に終端用の1マスを追加
        self.size = tuple(n + 1 for n in shape)

        # 多次元座標を1次元インデックスに変換
        self.stride = [1] * self.d
        for i in range(self.d - 2, -1, -1):
            self.stride[i] = self.stride[i + 1] * self.size[i + 1]

        total = 1
        for n in self.size:
            total *= n

        self.diff = [0] * total
        self.built = False

        # 各頂点の選択軸と符号を事前計算
        self.masks = [
            (
                tuple(i for i in range(self.d) if mask >> i & 1),
                -1 if mask.bit_count() & 1 else 1,
            )
            for mask in range(1 << self.d)
        ]

    def index(self, pos):
        return sum(p * s for p, s in zip(pos, self.stride))

    def add(self, left, right, value=1):
        """超直方体 [left, right) にvalueを加算"""
        if self.built:
            raise RuntimeError("build() 後は add() できません")

        base = self.index(left)
        offsets = [(r - l) * s for l, r, s in zip(left, right, self.stride)]

        diff = self.diff

        for axes, sign in self.masks:
            idx = base
            for axis in axes:
                idx += offsets[axis]

            diff[idx] += sign * value

    def build(self):
        """各軸に沿って累積和を取り、値を復元"""
        if self.built:
            return

        diff = self.diff

        for step, width in zip(self.stride, self.size):
            block = step * width

            for start in range(0, len(diff), block):
                for idx in range(start + step, start + block):
                    diff[idx] += diff[idx - step]

        self.built = True

    def get(self, pos):
        """指定座標の値を取得。build() 後のみ"""
        if not self.built:
            raise RuntimeError("先に build() を実行してください")

        return self.diff[self.index(pos)]


if __name__ == "__main__":
    # 3 × 4 × 5 の三次元空間
    imos = ImosND((3, 4, 5))

    # [0,2) × [1,3) × [2,5) に +7
    imos.add((0, 1, 2), (2, 3, 5), 7)

    imos.build()

    print(imos.get((1, 2, 3)))  # 7
    print(imos.get((2, 2, 3)))  # 0
