# N(<=10)進法の文字列に変換する関数
def to_base(n: int, base: int) -> str:
    if n == 0:
        return "0"

    digits = []
    while n:
        digits.append(str(n % base))
        n //= base

    return "".join(reversed(digits))
