from numpy import array
class Dot:
     #Возможые состояния status 1 (спокойная вода) и 0 (после попадания)
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self._status = 1
    @property
    def coord(self):
        return [self.x, self.y]
    def status(self):
        return self._status
    def shot(self):
        self._status = 0
    def print(self):
        return '~' if self._status == 1 else '@'

class Deck(Dot):
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self._status = 1
    def print(self):
        return "#" if self._status == 1 else '*'

class Ship:
    def __init__(self, x, y, orient, type, name, field):
        self.x = x
        self.y = y
        self.orient = orient
        self.type = type
        self.name = name
        self.field = field
        if orient == 1:
            for l in range(TYPEDICT.get(type)):
                field.setdot(y-1,x+l-1,Deck(x,y,name))
        else:
            for l in range(TYPEDICT.get(type)):
                field.setdot(y+l-1,x-1,Deck(x,y,name))

    # @property
    # def coord(self):
    #     return self.coordoc
    # def status(self, x, y):
    #     return self.coordoc[x, y]
    # def shot(self, x, y):
    #     self.coordoc[x, y] = 0

class Field:
    def __init__(self, l1, l2):
        self.sea = array([[Dot(i, j) for i in range(l1)] for j in range(l2)])
    @property
    def lookup(self):
        return self.sea
    def shoot(self, x, y):
        self.sea[y-1,x-1].shot()
    def setdot(self, y, x, obj):
        self.sea[y, x] = obj




TYPEDICT = { "battleship": 3, "destroyer": 2, "gunboat": 1 }
f1 = Field(6,6)
#print(*[f' {x.print()} ' for x in f1.sea[1]])

def main():
    print('Игра Морской Бой!')
    #Вывод поля
    print('       1   2   3   4   5   6')
    print('----------------------------')
    for i in range(6):
        print(i+1, ' | ', *[f' {x.print()} ' for x in f1.lookup[i]])

main()
f1.shoot(3,2)
main()
s1 = Ship(2, 3, 2, 'battleship', 'Linkor1', f1)
main()