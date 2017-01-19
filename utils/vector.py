import math


class Vector:  # represents 2D vector

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def lengthSquared(self):
        return self.x ** 2 + self.y ** 2

    def length(self):
        return math.sqrt(self.lengthSquared())

    def normalized(self):
        l = self.length()
        return self / self.length()

    def __add__(self, vec2):
        return Vector(self.x + vec2.x, self.y + vec2.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __sub__(self, vec2):
        return self + -vec2

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        return self * (1.0 / scalar)
