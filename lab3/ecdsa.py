from typing import Optional
from lab1 import randprime_functions as fp
import lab2.signature
import lab3
from lab2.signature import Signature
from lab3.curve_point import CurvePoint, reverse_by_mod
import hashlib
import lab1.randprime_functions as rf


class Curve:
    def __init__(self, a, b, g, n, h, p):
        self.a = a
        self.b = b
        self.g: CurvePoint = g
        self.n = n
        self.h = h
        self.p = p


CURVE: Curve = None


class ECDSASystem:
    def __init__(self, dimension, file_path):
        self.file_path = file_path
        self.dimension = dimension

    def generate_keys(self):
        private_key = fp.lib_randprime(1, CURVE.n - 1)
        public_key = CURVE.g.mul_on_scalar(private_key)
        return public_key, private_key

    def create_signature(self, private_key):
        hash_value = self.__get_hash_clip(self.__get_file_hash())
        while True:
            k = rf.lib_randprime(1, CURVE.n - 1)
            point = CURVE.g.mul_on_scalar(k)
            r = point.x % CURVE.n
            if r == 0:
                continue
            s = (reverse_by_mod(k, CURVE.n) * (hash_value + r * private_key)) % CURVE.n
            if s == 0:
                continue
            return Signature(r, s)

    def is_invalid_signature(self, signature: Signature, public_key: CurvePoint):
        hash_value = self.__get_hash_clip(self.__get_file_hash())
        w = reverse_by_mod(signature.s, CURVE.n)
        u = (w * hash_value) % CURVE.n
        v = (w * signature.r) % CURVE.n
        p = CURVE.g.mul_on_scalar(u) + public_key.mul_on_scalar(v)
        return signature.r % CURVE.n == p.x % CURVE.n

    def __get_hash_clip(self, hash_value):
        result = hash_value >> (hash_value.bit_length() - CURVE.n.bit_length())
        assert result.bit_length() <= CURVE.n.bit_length()
        return result

    def __get_file_hash(self, show_debug_messages=False):
        if show_debug_messages:
            print('DEBUG: Start hashing file.')
        file_hash = hashlib.sha256()
        with open(self.file_path, 'r') as file_in:
            file_hash.update(file_in.read().encode('utf-8'))
        result = int(file_hash.hexdigest(), 16)
        if show_debug_messages:
            print('DEBUG: Finish hashing file.')
        return result

    def load_sign_from_file(self):
        with open('sign_{}'.format(self.file_path), 'r') as file_in:
            r, s, x, y = map(int, file_in.readlines())
            file_in.close()
        if lab3.util.show_debug_messages:
            print('DEBUG: Signature loaded.')
        return Signature(r, s), CurvePoint(x, y)

    def save_sign_to_file(self, signature: Signature, pk: CurvePoint):
        with open('sign_{}'.format(self.file_path), 'w') as file_out:
            file_out.write('{}\n{}\n{}\n{}'.format(signature.r, signature.s, pk.x, pk.y))
            file_out.close()
        if lab3.util.show_debug_messages:
            print('DEBUG: Signature saved.')
