from ..Eratosthenes.Eratosthenes import Eratosthenes
from math import isqrt


class PrimeFactorizer:
    def __init__(self, sieve: Eratosthenes):
        self.sieve = sieve

    def factorize(self, n: int) -> list[tuple[int, int]]:
        """1 <= n <= sieve.limit**2 の完全な素因数分解"""

        M = self.sieve.limit

        if n < 1 or n > M * M:
            raise ValueError("n is outside the supported range")

        if n <= M:
            return self.sieve.factorize(n)

        res = []

        for p in self.sieve.primes:
            # 残りが篩の範囲内なら高速分解に切り替える
            if n <= M:
                res.extend(self.sieve.factorize(n))
                return res

            # 残りは素数
            if p * p > n:
                res.append((n, 1))
                return res

            if n % p != 0:
                continue

            exp = 0
            while n % p == 0:
                n //= p
                exp += 1

            res.append((p, exp))

        # 試し割りで全て割り切った場合
        if n > 1:
            if n <= M:
                res.extend(self.sieve.factorize(n))
            else:
                # n <= M**2 の保証により残りは素数
                res.append((n, 1))

        return res


if __name__ == "__main__":
    N = 100
    sieve = Eratosthenes(isqrt(N) + 1)
    factorizer = PrimeFactorizer(sieve)

    k = sum(exp for _, exp in factorizer.factorize(N))
    print((k - 1).bit_length())
