"""
iterableに含まれる要素の数を簡単に数えることができる。便利。
"""

from collections import Counter

A = [1, 2, 1, 3, 2, 1]
cnt = Counter(A)
print(cnt)
# Counter({1: 3, 2: 2, 3: 1})
print(cnt[1])
# 3
print(cnt[2])
# 2
