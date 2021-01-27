from numpy import array
from icecream import ic
class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Выстрел за пределы доски!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Точка уже поражена!"

class WrongShipSetting(BoardException):
    def __str__(self):
        return "Корабль не может быть размещен в заданной точке!"

class Dot:
     #Возможые состояния status 1 (спокойная вода) и 0 (после попадания)
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self._status = 1
        self.occupied = 0
    @property
    def coord(self):
        return [self.x, self.y]
    @property
    def status(self):
        return self._status
    def shot(self, field):
        if self._status == 0:
            raise BoardUsedException()
        else:
            self._status = 0
    @property
    def occ_state(self):
        return self.occupied
    def set_occ(self):
        if self.occupied == 1:
            raise WrongShipSetting()
        else:
            self.occupied = 1
    def print(self):
        return '~' if self._status == 1 else '.'

class Deck(Dot):
    def __init__(self, x, y, name, visible):
        self.x = x
        self.y = y
        self.name = name
        self._status = 1
        self.occupied = 1
        self.visible = visible
    def shot(self, field):
        if self._status == 0:
            raise BoardUsedException()
        else:
            self._status = 0
            field.checkship(self.name)

    def print(self):
        if self.visible == 1:
            return "#" if self._status == 1 else '*'
        else:
            return "~" if self._status == 1 else '*'


class Ship:
    def __init__(self, x, y, orient, type, name, field, visible):
        self.x = x
        self.y = y
        self.orient = orient
        self.type = type
        self.name = name
        self.field = field
        if orient == 1:
            for l in range(TYPEDICT.get(type)):
                field.setdot(y-1,x+l-1,Deck(x,y,self, visible), self)
        else:
            for l in range(TYPEDICT.get(type)):
                field.setdot(y+l-1,x-1,Deck(x,y,self, visible), self)
    def name(self):
        return self.name
    def contour(self):
        pass


# Создание корабля помещает его имя в дочернние точки и словарь кораблей в игровом поле. При попадании в точку метод запускает проверку остатка живых точек в корабле.
# Если точки в корабле остались кричим, что ранили. Если нет, убили, и запскаем процесс оконтуривания с включением видимости.

class Field:
    def __init__(self, l1, l2):
        self.sea = array([[Dot(i, j) for i in range(l1)] for j in range(l2)])
        self.shipdict = dict()
    @property
    def lookup(self):
        return self.sea
    def shoot(self, x, y):
        self.sea[y-1,x-1].shot(self)
    def checkship(self, name):
        print(self.shipdict.get(name))
        _ = [i.status for i in self.shipdict.get(name)]
        print(_)
        if 1 in _:
            print('Корабль ранен!')
        else:
            print(f'Вы уничтожили {name.name}!')
            name.contour()
    def setdot(self, y, x, obj, shipname):
        if self.sea[y,x].occ_state == 1:
            raise WrongShipSetting()
        else:
            self.sea[y, x] = obj
            if self.shipdict.get(shipname):
                self.shipdict[shipname].append(obj)
            else:
                d1 = {shipname:[obj]}
                self.shipdict.update(d1)

            # for i in range(y-1, y+2):
            #     for j in range(x-1, x+2):
            #         self.sea[i, j].set_occ()




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

#f1.shoot(3,2)
main()
s1 = Ship(3, 3, 2, 'battleship', 'Linkor1', f1, 1)
main()
print(f1.shipdict)
f1.shoot(3,3)
f1.shoot(3,5)

main()
#Нужно сделать оконтуривания статусом occupied по словарю корабля!
# Нужно не забыть про видимость!