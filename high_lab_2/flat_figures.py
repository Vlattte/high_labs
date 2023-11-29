from abc import ABC, abstractmethod


class Figure(ABC):
    @abstractmethod
    def square(self):
        pass


class Rectangle(Figure):
    name = "Rectangle"

    def __init__(self, border, height):
        self.border = border
        self.height = height

    def square(self):
        return self.border * self.height


class Triangle(Figure):
    name = "Triangle"

    def __init__(self, border, height):
        self.border = border
        self.height = height

    def square(self):
        return self.border * self.height * 0.5


class Circle(Figure):
    name = "Circle"

    def __init__(self, radius):
        self.radius = radius

    def square(self):
        return 3.14159 * self.radius ** 2


if __name__ == "__main__":
    # Circle
    cir = Circle(4)
    print(cir.name)
    print(cir.square())

    # Triangle
    tri = Triangle(1, 2)
    print(tri.name)
    print(tri.square())

    # Rectangle
    rec = Rectangle(1, 2)
    print(rec.name)
    print(rec.square())