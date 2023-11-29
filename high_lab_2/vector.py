from math import sqrt

class Vector:
    def __init__(self, x=1, y=1):
        self.x = x
        self.y = y

    def __eq__(self, other):
        xEq = self.x == other.x
        yEq = self.y == other.y
        return xEq and yEq

    def __ne__(self, other):
        xNeq = self.x != other.x
        yNeq = self.y != other.y
        return xNeq and yNeq

    def __abs__(self):
        return sqrt(self.x**2+self.y**2)

    def __str__(self):
        return "<{}; {}>".format(self.x, self.y)

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        vec_x = self.x + other.x
        vec_y = self.y + other.y
        return Vector(vec_x, vec_y)

    def __sub__(self, other):
        vec_x = self.x - other.x
        vec_y = self.y - other.y
        return Vector(vec_x, vec_y)

    def __mul__(self, other):
        if type(other) == Vector:
            """ DOT PROD """
            return self.x * other.x + self.y * other.y
        elif type(other) == int or type(other) == float:
            """ MULTIPLY WITH CONSTANT"""
            vec_x = self.x * other
            vec_y = self.y * other
            return Vector(vec_x, vec_y)
        return Exception("WRONG TYPE OF SECOND ARGUMENT")

if __name__ == "__main__":
    # init
    v1 = Vector()
    print(v1)
    v2 = Vector(4, 0)
    print(v2)

    # equal
    print("\nequal: " + str(v1==v2))
    print("equal: " + str(v1==v1))

    # not equal
    print("\nnot equal: " + str(v1!=v2))
    print("not equal: " + str(v1!=v1))

    # add
    print("\nadd: " + str(v1+v2))
    print("add: " + str(v2+v1))

    # sub
    print("\nsub: " + str(v1-v2))
    print("sub: " + str(v2-v1))

    # mul
    print("\nmul: " + str(v1*v2))
    print("mul: " + str(v2*v1))
    print("mul: " + str(v1*10))
    print("mul: " + str(v1*6))

    # abs
    print("\nabs: " + str(abs(v1)))
    print("abs: " + str(abs(v2)))