from typing import Tuple, List
from math import sqrt

import random as rn
import math
from typing import Tuple, List

mr_round_count = 128
show_debug_messages = True


def advanced_gcd(a: int, b: int) -> Tuple[int, int, int]:
    xx, yy = 0, 1
    x, y = 1, 0
    while b:
        q = a // b
        a, b = b, a % b
        x, xx = xx, x - xx * q
        y, yy = yy, y - yy * q
    return a, x, y


def trivial_division_test_function(n: int) -> bool:
    if show_debug_messages:
        print("DEBUG: Start The trivial division prime testing.")
    if n % 2 == 0:
        return False
    sqrt_n = int(sqrt(n))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True


def jacobi(m: int, n: int) -> int:
    """
    Returns the Jacobi symbol `(m / n)`.

    For any integer ``m`` and any positive odd integer ``n`` the Jacobi symbol
    is defined as the product of the Legendre symbols corresponding to the
    prime factors of ``n``"""
    if n < 0 or not n % 2:
        raise ValueError("n should be an odd positive integer")
    if m < 0 or m > n:
        m = m % n
    if not m:  # m == 0
        return int(n == 1)
    if n == 1 or m == 1:
        return 1
    if advanced_gcd(m, n)[0] != 1:  # gcd(m, n) == 1
        return 0

    j = 1
    if m < 0:
        m = -m
        if n % 4 == 3:
            j = -j
    while m != 0:
        while m % 2 == 0 and m > 0:
            m >>= 1
            if n % 8 in [3, 5]:
                j = -j
        m, n = n, m
        if m % 4 == 3 and n % 4 == 3:
            j = -j
        m %= n
    if n != 1:
        j = 0
    return j


def solovay_strassen_test_function(n: int, rounds_count: int) -> bool:
    if show_debug_messages:
        print("DEBUG: Start The Solovay-Strassen prime testing.")
    for i in range(1, rounds_count + 1):
        if show_debug_messages:
            print("DEBUG: Round {} from {}".format(i, rounds_count))
        a = rn.randint(2, n - 2)
        r = pow(a, (n - 1) // 2, n)
        if r != 1 and r != n - 1:
            return False
        s = jacobi(a, n)
        if r != s % n:
            return False
    return True


def miller_rabin_test_function(rand_number: int, rounds_count: int) -> bool:
    if show_debug_messages:
        print("DEBUG: Start The Miller-Rabin prime testing.")
    if rand_number % 2 == 0:
        return False
    t = rand_number - 1
    s = 0
    while t % 2 == 0:
        t >>= 1
        s += 1
    for i in range(1, rounds_count + 1):
        if show_debug_messages:
            print("DEBUG: Round {} from {}".format(i, rounds_count))
        a = rn.randint(2, rand_number - 2)
        y = pow(a, t, rand_number)
        if y == 1 or y == rand_number - 1:
            continue
        flag = False
        for j in range(0, s):
            y = pow(y, 2, rand_number)
            if y == 1:
                return False
            if y == rand_number - 1:
                flag = True
                break
        if flag:
            continue
        return False
    return True
