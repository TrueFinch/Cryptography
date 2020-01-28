from typing import Callable
from lab1 import util


class Rsa:
    def __init__(self, prime_number_generation_function: Callable, max_key_length: int, chunk_size, byteorder):
        self.__byteorder = byteorder
        self.__chunk_size = chunk_size
        self.max_key_length = max_key_length
        self.__maxBorder = 2 ** self.max_key_length
        self.__minBorder = 2 ** (self.max_key_length >> 1)
        self.__prime_number_generation_function = prime_number_generation_function
        p = self.__generate_random_prime()
        q = self.__generate_random_prime()
        self.max_length = 0
        # module
        self.n = p * q
        u = (p - 1) * (q - 1)
        # opened key
        self.e = self.__calculate_e(u)
        # closed key
        self.d = self.__calculate_d(self.e, u)

    def __generate_random_prime(self) -> int:
        result: int = 0
        result = self.__prime_number_generation_function(self.__minBorder, self.__maxBorder)
        return result

    # u: euler function of module
    @staticmethod
    def __calculate_e(u: int) -> int:
        return 65537

    def __calculate_d(self, e: int, u: int) -> int:
        d, x, y = util.advanced_gcd(e, u)
        return x if x > 0 else x + u

    # code: character code to encode,
    def __encode_chunk(self, code: int) -> int:
        return pow(code, self.e, self.n)

    # string: string to encode
    def encode_bytes(self, a_bytes: bytes) -> int:
        # result = []
        # self.max_length = 0
        #
        # for char in a_bytes:
        #     result.append(str(self.__encode_chunk(ord(char))))
        #     self.max_length = max(self.max_length, len(result[-1]))
        #
        # for i, code in enumerate(result):
        #     if self.max_length > len(code):
        #         result[i] = ("0" * (self.max_length - len(code))) + code

        return self.__encode_chunk(int.from_bytes(a_bytes, byteorder=self.__byteorder))

    # code: encrypted character code to decode
    def __decode_chunk(self, code: int) -> int:
        return pow(code, self.d, self.n)

    # string: string of encrypted characters to decode
    def decode_bytes(self, code: int) -> bytes:
        # codes = [(string[i:i + self.max_length]) for i in range(0, len(string), self.max_length)]
        # result = ""
        # for code in codes:
        #     if len(code) < self.max_length:
        #         return -1, ""
        #     result += chr(self.__decode_chunk(int(code)))

        return self.__decode_chunk(code).to_bytes(self.__chunk_size, byteorder=self.__byteorder)
