from rect_class import Rectangle, Square, Circle

rect_1 = Rectangle(4,10)
rect_2 = Rectangle(7,5)

# print(rect_1.getArea())
# print(rect_2.getArea())

square_1 = Square(6)
square_2 = Square(5)

# print(square_1.getAreaSq())
# print(square_2.getAreaSq())

circ_1 = Circle(6)
circ_2 = Circle(3)

figures = [rect_2, rect_1, square_1, square_2, circ_1, circ_2]

for i in figures:
    if isinstance(i, Square):
        print(i.getAreaSq())
    else:
        print(i.getArea())

