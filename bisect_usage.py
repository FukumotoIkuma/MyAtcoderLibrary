"""
ソート済み配列から、指定した値を挿入できる最も左の位置を O(log N) で求められる。
pythonにおける二分探索はbisectライブラリを用いるのが簡単である。

"""

from bisect import bisect_left, bisect_right


A = [1, 3, 3, 3, 5, 7]

print(bisect_left(A, 3))  # 3 未満の要素数
# 1
print(bisect_right(A, 3))  # 3 以下の要素数
# 4


"""
key = funcを指定することで、配列の各要素を遅延初期化することも可能。
ただし生成される配列が単調増加である必要があるので注意。
典型的には最小値の最大化(最大値の最小化)などの問題で使いやすい。
"""
# https://atcoder.jp/contests/typical90/tasks/typical90_a

# 以下の様な配列を想定し、False -> Trueへの変化点を探すイメージ
# L[i]はその最小値が不可能かどうか。不可能-> True, 可能-> False
# L = [False, False, False, True, True]
# 100までの中に最小値があるとして、最小値の最大値を求める場合は以下
# 各探索ではその数は最小値の可能性があるかを確かめる（最小値であるかではない）


def impossible(x):
    # heavy impl
    return False / True


N = 100
result = bisect_left(range(N), True, key=impossible) - 1


"""
使う可能性は少ないだろうが、挿入するメソッドもある
"""
from bisect import insort, insort_left, insort_right

A = [1, 3, 3, 5]

insort(A, 4)
print(A)  # [1, 3, 3, 4, 5]

"""
left と right の違い
- insort_left：同じ値の左側に挿入
- insort_right：同じ値の右側に挿入
- insort：insort_right と同じ
計算量
操作	計算量
挿入位置の探索	(O(log N))
要素の挿入	(O(N))
insort 全体	(O(N))
使い分け：
- 少数の挿入 → insort
- 全要素をまとめてソート → sort()
- 最小値の管理 → heapq
"""
