import lab3
from lab3.ecdsa import *
from lab3.util import reverse_by_mod, get_next_bit


class CurvePoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_zero = x == 0 and y == 0

    def mul_on_scalar(self, scalar: int):
        if scalar % lab3.ecdsa.CURVE.n == 0 or self.is_zero:
            return CurvePoint(0, 0)
        if scalar < 0:
            return self.neg().mul_on_scalar(-scalar)
        point = CurvePoint(self.x, self.y)
        result = CurvePoint(0, 0)
        for bit in get_next_bit(scalar):
            if bit == 1:
                result += point
            point += point
        return result

    def neg(self):
        if self.is_zero:
            return CurvePoint(0, 0)
        return CurvePoint(self.x, -self.y % lab3.ecdsa.CURVE.p)

    def __add__(self, other):
        if self.is_zero:
            return other
        if other.is_zero:
            return self
        if self.x == other.x and self.y != other.y:
            return CurvePoint(0, 0)

        m = (3 * pow(self.x, 2) + lab3.ecdsa.CURVE.a) * reverse_by_mod(2 * self.y, lab3.ecdsa.CURVE.p) \
            if self == other else (self.y - other.y) * reverse_by_mod(self.x - other.x, lab3.ecdsa.CURVE.p)
        x = (m * m - self.x - other.x) % lab3.ecdsa.CURVE.p
        y = (self.y + m * (x - self.x)) % lab3.ecdsa.CURVE.p
        return CurvePoint(x, -y)

    def __eq__(self, other: 'CurvePoint'):
        return self.is_zero and other.is_zero or self.x == other.x and self.y == other.y

    def __ne__(self, other: 'CurvePoint'):
        if self.is_zero and not other.is_zero or not self.is_zero and other.is_zero:
            return True
        if self.is_zero and other.is_zero:
            return False
        return self.x != other.x or self.y != other.y
