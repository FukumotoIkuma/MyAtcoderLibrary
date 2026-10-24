"""
[エラトステネスの篩の活用法を総特集！ 〜 高速素因数分解・メビウスの反転公式 〜](https://qiita.com/drken/items/3beb679e54266f20ab63)
"""

from array import array


class Eratosthenes:
    def __init__(self, N):
        # テーブル
        self.isprime: bytearray = bytearray([1]) * (N + 1)

        # 整数 i を割ることのできる最大の素数
        self.maxfactor = [-1] * (N + 1)

        # メビウス関数
        self.mobius = array("b", [1]) * (N + 1)

        # 0, 1 は素数ではない
        self.isprime[0] = 0
        if N >= 1:
            self.isprime[1] = 0
            self.maxfactor[1] = 1

        # 篩
        for p in range(2, N + 1):
            # すでに合成数ならスキップ
            if not self.isprime[p]:
                continue

            # メビウス: p の倍数は符号反転
            for q in range(p, N + 1, p):
                self.mobius[q] *= -1

            if p**2 <= N:
                # p の倍数をふるい落とす
                self.isprime[p**2 : N + 1 : p] = bytes((N - p**2) // p + 1)

                # メビウス: p**2 の倍数は 0
                self.mobius[p**2 : N + 1 : p**2] = array("b", [0]) * (N // (p**2))

            # 最大素因数を記録
            self.maxfactor[p : N + 1 : p] = [p] * (N // p)

    # 高速素因数分解
    # (素因子,指数) の素因子昇順リストを返す
    def factorize(self, n) -> list[tuple[int, int]]:
        res = []

        while n > 1:
            p = self.maxfactor[n]
            exp = 0

            while n > 1 and self.maxfactor[n] == p:
                n //= p
                exp += 1

            res.append((p, exp))

        res.reverse()
        return res

    # 高速約数列挙
    # 約数のリストを返す（昇順ではない）
    def divisors(self, n) -> list[int]:
        res = [1]

        # 素因数分解
        pf = self.factorize(n)

        # 約数列挙
        for p, exp in pf:
            s = len(res)
            for i in range(s):
                v = 1
                for _ in range(exp):
                    v *= p
                    res.append(res[i] * v)

        return res

    def lcm_factors(self, A: list[int]) -> dict[int, int]:
        """複数整数の最小公倍数を素因数分解形式で返す
        {素因子: 最大指数}"""
        res = {}

        for a in A:
            for p, exp in self.factorize(a):
                res[p] = max(res.get(p, 0), exp)

        return res

    @staticmethod
    def factor_product(factors: dict[int, int], mod: int | None = None) -> int:
        """素因数分解形式から整数を復元する。mod指定時は剰余を返す"""
        ans = 1

        for p, exp in factors.items():
            if mod is None:
                ans *= pow(p, exp)
            else:
                ans = ans * pow(p, exp, mod) % mod

        return ans


# 高速ゼータ変換
# 入力 f が in-place に更新されて、F になる
# ゼータ変換は多次元累積和をとる処理となっているため、これを用いて高速に処理できる
# 素数を各次元方向に対応させる。三次元における点(a,b,c)はf[2**a * 3**b * 5 **c]に位置する
def fast_zeta(f: list[int]) -> None:
    N = len(f)

    # エラトステネスの篩を用いて素数を列挙
    # <<<何度も呼び出すならこれは引数の方がいいかも>>>
    isprime = Eratosthenes(N).isprime

    # 各素数 p 軸に対して
    # 大きい座標 (k * p) から小さい座標 (k) へと足し込む
    for p in range(2, N):
        if not isprime[p]:
            continue

        # 座標が大きい方を起点として累積和をとる
        for k in range((N - 1) // p, 0, -1):
            f[k] += f[k * p]


def fast_mobius(F: list[int]) -> None:
    N = len(F)

    # エラトステネスの篩を用いて素数を列挙
    # <<<何度も呼び出すならこれは引数の方がいいかも>>>
    isprime = Eratosthenes(N).isprime

    # 各素数 p 軸に対して
    # 小さい座標 (k) から大きい座標 (k * p) を引いていく

    for p in range(2, N):
        if not isprime[p]:
            continue

        for k in range(1, (N - 1) // p + 1):
            # 座標が小さい方を起点として差分をとる
            F[k] -= F[k * p]


def main():
    er = Eratosthenes(50)

    for n in range(2, 51):
        pf = er.factorize(n)
        print(f"{n}: " + " * ".join(f"{p}^{exp}" for p, exp in pf))

    # 高速約数列挙
    print(er.divisors(12))  # [1, 2, 4, 3, 6, 12]
    print(er.divisors(36))  # [1, 2, 4, 3, 6, 12, 9, 18, 36]
    print(er.divisors(1))  # [1]

    # メビウス関数の値を取得
    print(er.mobius[1])  # 1
    print(er.mobius[2])  # -1

    # 高速ゼータ変換
    f = [0] + list(range(1, 13))
    fast_zeta(f)
    print(f[1:])
    # [78, 42, 30, 24, 15, 18, 7, 8, 9, 10, 11, 12]

    # 高速メビウス変換（逆変換）
    fast_mobius(f)
    print(f[1:])
    # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


if __name__ == "__main__":
    main()
