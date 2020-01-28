from lab1 import util
import sympy as sp
import random


def get_odd_rand(min, max):
    r = random.randrange(min, max + 1)
    return r + ~(r & 1)


def find_randprime(min, max, is_prime):
    rand_number = get_odd_rand(min, max)
    while not is_prime(rand_number):
        print("DEBUG: {} is not prime.".format(rand_number))
        rand_number = get_odd_rand(min, max)

    print("DEBUG: {} is prime.".format(rand_number))
    return rand_number


def lib_randprime(min, max):
    rand_number = sp.randprime(min, max)
    print("DEBUG: {} is prime.".format(rand_number))
    return rand_number


def td_randprime(min: int, max: int):
    return find_randprime(min, max, lambda x: util.trivial_division_test_function(x))


def ss_randprime(min: int, max: int):
    return find_randprime(min, max, lambda x: util.solovay_strassen_test_function(x, util.mr_round_count))


def mr_randprime(min: int, max: int):
    return find_randprime(min, max, lambda x: util.miller_rabin_test_function(x, util.mr_round_count))
