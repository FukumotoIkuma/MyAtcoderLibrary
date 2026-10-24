"""
円環に対する尺取法や区間和
"""

# A: 長さNの円環配列
A = [(0, -1), (-1, 1), (1, 0), (0, 1)]
N = len(A)


def condition(i, j):
    return True


A = sorted(A)  # 尺取なので条件が単調に変化することを保証する必要がある
A = A + A
j = 0
ans = 0
for i in range(N):
    j = max(j, i)

    while j < i + N and condition(i, j):
        j += 1

    # [i, j) が条件を満たす区間
    # 答えを更新する
    ans = j - i

    # 必要なら、A[i] を区間の管理情報から除く

"""
区間和：円環上で、合計が K 以下になる最長の連続区間など
"""
A = [1, 3, 4, 2, 4, 7, 1]
B = A * 2
K = 3
j = 0
total = 0
ans = 0

for i in range(N):
    while j < i + N and total + B[j] <= K:
        total += B[j]
        j += 1

    ans = max(ans, j - i)

    if i < j:
        total -= B[i]
    else:
        j = i + 1
