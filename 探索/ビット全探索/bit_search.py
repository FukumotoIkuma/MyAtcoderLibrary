"""二通りの値で表せる物を全列挙する時につかう。辞書順だから便利。
概念的にはＮ進法に拡張できる
枝刈りとか考えるとDFSのほうが良いという話になるかもしれない
"""

# N桁の全列挙とする
N = 20

for i in range(1 << N):
    # 上のdigitから見ていく（多くの場合その方が都合がいいだけ）
    for j in range(N - 1, -1, -1):
        digit = (i >> j) & 1

        # do something


"""B進法の場合"""

B = 3
powers = [1] * N

# 毎回計算すると重いのであらかじめ計算する
for j in range(1, N):
    powers[j] = powers[j - 1] * B

# B進法全探索
for i in range(B**N):
    x = i
    for j in range(N - 1, -1, -1):
        digit = x // powers[j]
        x %= powers[j]

        # do something
