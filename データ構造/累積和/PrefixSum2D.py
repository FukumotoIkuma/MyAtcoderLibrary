class PrefixSum2D:
    """二次元累積和。長方形 [y1, y2) × [x1, x2) の合計を取得する。"""

    def __init__(self, A: list[list[int]]):
        H, W = len(A), len(A[0])
        self.H = H
        self.W = W

        S = [[0] * (W + 1) for _ in range(H + 1)]

        for y in range(H):
            for x in range(W):
                S[y + 1][x + 1] = A[y][x] + S[y][x + 1] + S[y + 1][x] - S[y][x]

        self.S = S

    def get(self, left: tuple[int, int], right: tuple[int, int]) -> int:
        """長方形 [left, right) の合計"""
        y1, x1 = left
        y2, x2 = right
        S = self.S

        return S[y2][x2] - S[y1][x2] - S[y2][x1] + S[y1][x1]


if __name__ == "__main__":
    A = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]

    S = PrefixSum2D(A)

    print(S.get((0, 0), (2, 2)))  # 12
    print(S.get((1, 1), (3, 3)))  # 28
    print(S.get((0, 0), (3, 3)))  # 45
