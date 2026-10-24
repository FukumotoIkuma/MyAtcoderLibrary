"""
Pythonにおいてはitertools.accumulateを用いることで簡便に計算することができる。
また、一般的に累積和の各要素iはは [0,i)の範囲を表すため、initial引数を指定すべきである
累積最大/最小値も同様にして簡便に求めることができる
"""

from itertools import accumulate

A = [3, 1, 4, 2]

# 累積和
print(list(accumulate(A, initial=0)))
# [0, 3, 4, 8, 10]

# 累積最大値
print(list(accumulate(A, max, initial=-float("inf"))))
# [-inf, 3, 3, 4, 4]

# 累積最小値
print(list(accumulate(A, func=min, initial=float("inf"))))
# [inf, 3, 1, 1, 1]

# 右から累積最小値(オプションは無いらしい）
print(list(accumulate(reversed(A), min, initial=float("inf")))[::-1])
# [1, 1, 2, 2, inf]
