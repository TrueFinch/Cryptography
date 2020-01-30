from typing import Tuple
import lab1.randprime_functions as rf
from lab1.util import show_debug_messages
import hashlib
import lab1
import lab2.util


class ElGamalKey:
    def __init__(self, key, generator, prime):
        self.key = key
        self.generator = generator
        self.prime = prime


class Signature:
    def __init__(self, r, s):
        self.r = r
        self.s = s


class ElGamalSignature(Signature):
    def __init__(self, r, s):
        super().__init__(r, s)


class ElGamalSystem:
    def __init__(self, dimension, file_path):
        self.__dimension = dimension
        self.__file_path = file_path

    def generate_keys(self):
        while True:
            prime = rf.lib_randprime(2 ** (self.__dimension >> 2), 2 ** (self.__dimension - 1))
            safeprime = 2 * prime + 1
            if lab1.util.miller_rabin_test_function(safeprime, lab1.util.mr_round_count):
                break

        while True:
            generator = rf.lib_randprime(3, safeprime - 2)
            if pow(generator, 2, safeprime) != 1 and pow(generator, prime, safeprime) != 1:
                break

        private_key = ElGamalKey(rf.lib_randprime(2, safeprime - 2), generator, safeprime)
        public_key = ElGamalKey(pow(generator, private_key.key, safeprime), generator, safeprime)
        return public_key, private_key

    def create_signature(self, private_key: ElGamalKey):
        file_hash_value = self.__get_file_hash(show_debug_messages)
        coprime = lab2.util.generate_random_coprime(private_key.prime - 1)
        r = pow(private_key.generator, coprime, private_key.prime)
        s = ((file_hash_value - private_key.key * r) * lab2.util.reverse_by_mod(coprime, private_key.prime - 1)) \
            % (private_key.prime - 1)
        return ElGamalSignature(r, s)

    def is_invalid_signature(self, sign: ElGamalSignature, pk: ElGamalKey):
        if not ((0 < sign.r < pk.prime) and (0 < sign.s < pk.prime - 1)):
            return False
        hash_value = self.__get_file_hash(show_debug_messages)
        return pow(pk.generator, hash_value, pk.prime) == (
                pow(pk.key, sign.r, pk.prime) * pow(sign.r, sign.s, pk.prime)) % pk.prime

    def save_sign_to_file(self, signature: ElGamalSignature, pk: ElGamalKey):
        with open('sign_{}'.format(self.__file_path), 'w') as file_out:
            file_out.write('{}\n{}\n{}\n{}\n{}'.format(signature.r, signature.s, pk.key, pk.generator, pk.prime))
            file_out.close()
        if lab2.util.show_debug_messages:
            print('DEBUG: Signature saved.')

    def load_sign_from_file(self) -> Tuple[ElGamalSignature, ElGamalKey]:
        with open('sign_{}'.format(self.__file_path), 'r') as file_in:
            r, s, key, generator, prime = map(int, file_in.readlines())
            file_in.close()
        if lab2.util.show_debug_messages:
            print('DEBUG: Signature loaded.')
        return ElGamalSignature(r, s), ElGamalKey(key, generator, prime)

    def __get_file_hash(self, show_debug_messages=False):
        if show_debug_messages:
            print('DEBUG: Start hashing file.')
        file_hash = hashlib.sha256()
        with open(self.__file_path, 'r') as file_in:
            file_hash.update(file_in.read().encode('utf-8'))
        result = int(file_hash.hexdigest(), 16)
        if show_debug_messages:
            print('DEBUG: Finish hashing file.')
        return result
