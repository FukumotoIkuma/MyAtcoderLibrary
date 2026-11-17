"""
リスト/集合が大小関係持ってたら嬉しい場面があるよね
平衡二分探索木とか言ってるけど、要するにライブラリ使えばOK
詳しく平衡二分探索木そのもののアルゴリズムしりたいなら調べよう

なお、tleする場合はより高速な実装のコピペライブラリsortedset,sortedmultisetを確認
"""

from sortedcontainers import SortedDict, SortedList, SortedSet


# =================
s = SortedList()

s.add(3)
s.add(8)
s.add(5)

print(list(s))  # [3, 5, 8]

# =================
s = SortedList(key=lambda x: -x)

s.add(3)
s.add(8)
s.add(5)

print(list(s))  # [8, 5, 3]

# =================

s = SortedSet()
s.add(3)
s.add(8)
s.add(3)

print(list(s))  # [3, 8]

# =================
d = SortedDict()
d[10] = "a"
d[3] = "b"
d[7] = "c"

print(list(d))  # [3, 7, 10]
print(d.peekitem(1))  # (7, 'c')
