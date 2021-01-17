from math import pi
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height
    def getArea(self):
        return self.width * self.height

class Square:
    def __init__(self, side):
        self.side = side
    def getAreaSq(self):
        return self.side ** 2

class Circle:
    def __init__(self, radius):
        self.radius = radius
    def getArea(self):
        return pi * self.radius ** 2

class PosRectangle(Rectangle):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def getPosition(self):
        return self.x , self.y
    def __str__(self):
        return str(f' Rectangle ({self.x}, {self.y}, {self.width}, {self.height})')
