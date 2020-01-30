import lab3
from lab1.util import advanced_gcd

show_debug_messages = True


def get_next_bit(scalar):
    while scalar > 0:
        yield scalar & 1
        scalar >>= 1


def reverse_by_mod(k: int, p: int) -> int:
    if k < 0:
        return p - reverse_by_mod(-k, p)
    gcd, x, y = advanced_gcd(k, p)

    assert gcd == 1
    assert (k * x) % p == 1

    return x % p
