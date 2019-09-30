import sympy as sp
from typing import Tuple


class Rsa:
    def __init__(self):
        self.__maxBorder = 2 ** 1024
        self.__minBorder = 2 ** 512
        p = sp.randprime(self.__minBorder, self.__maxBorder)
        q = sp.randprime(self.__minBorder, self.__maxBorder)
        self.max_length = 0
        # module
        self.n = p * q
        u = (p - 1) * (q - 1)
        # opened key
        self.e = self.__calculate_e(u)
        # closed key
        self.d = self.__calculate_d(self.e, u)

    # u: euler function of module
    @staticmethod
    def __calculate_e(u: int) -> int:
        return 65537

    def __calculate_d(self, e: int, u: int) -> int:
        d, x, y = self.__advanced_gcd(e, u)
        return x if x > 0 else x + u

    # code: character code to encode,
    def __encode_char(self, code: int) -> int:
        return pow(code, self.e, self.n)

    # string: string to encode
    def encode_string(self, string: str) -> Tuple[int, str]:
        result = []
        self.max_length = 0

        for char in string:
            result.append(str(self.__encode_char(ord(char))))
            self.max_length = max(self.max_length, len(result[-1]))

        for i, code in enumerate(result):
            if self.max_length > len(code):
                result[i] = ("0" * (self.max_length - len(code))) + code

        return self.max_length, ''.join(result)

    # code: encrypted character code to decode
    def __decode_char(self, code: int) -> int:
        return pow(code, self.d, self.n)

    # string: string of encrypted characters to decode
    def decode_string(self, string: str) -> Tuple[int, str]:
        codes = [(string[i:i + self.max_length]) for i in range(0, len(string), self.max_length)]
        result = ""
        for code in codes:
            if len(code) < self.max_length:
                return -1, ""
            result += chr(self.__decode_char(int(code)))

        return self.max_length, result

    def __advanced_gcd(self, a: int, b: int) -> Tuple[int, int, int]:
        if a == 0:
            return b, 0, 1
        d, x1, y1 = self.__advanced_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return d, x, y
