import lab1.randprime_functions as rf
import lab1.util

show_debug_messages = True

coprime_round_count = 128


def generate_random_coprime(prime):
    for i in range(1, coprime_round_count + 1):
        result = rf.lib_randprime(2, prime - 1)
        gcd, _, _ = lab1.util.advanced_gcd(prime, result)
        if gcd == 1:
            return gcd
    return 65537


def reverse_by_mod(x: int, modulo: int):
    a, x, y = lab1.util.advanced_gcd(x, modulo)
    return (x % modulo + modulo) % modulo
