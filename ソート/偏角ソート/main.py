"""
座標平面上の原点意外に存在する点を0°以上360°未満の偏角の昇順にする
原点は偏角が定義できないので入力してはいけない。
"""

from functools import cmp_to_key


# O(N logN)
def angle_sort(P: list[tuple[int, int]]):
    def cross(a: tuple[int, int], b: tuple[int, int]):
        x1, y1 = a
        x2, y2 = b
        return x1 * y2 - y1 * x2

    def half(p: tuple[int, int]) -> int:
        x, y = p
        return 0 if y > 0 or (y == 0 and x > 0) else 1

    def angle_cmp(a, b):
        ha, hb = half(a), half(b)

        if ha != hb:
            return ha - hb

        c = cross(a, b)
        if c > 0:
            return -1
        if c < 0:
            return 1
        return 0

    return sorted(P, key=cmp_to_key(angle_cmp))


P = [(0, -1), (-1, 1), (1, 0), (0, 1)]

print(angle_sort(P))
