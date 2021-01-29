from numpy import array
from random import randint
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
    def coord(self):
        return (self.x, self.y)
    @property
    def status(self):
        return self._status
    def shot(self, field):
        if self._status == 0:
            raise BoardUsedException()
        else:
            self._status = 0
    def occupy(self):
        self.occupied = 1
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
    def __init__(self, x, y, shipname, visible):
        self.x = x
        self.y = y
        self.shipname = shipname
        self._status = 1
        self.occupied = 1
        self.visible = visible
    def coord(self):
        return (self.x, self.y)
    def shot(self, field):
        if self._status == 0:
            raise BoardUsedException()
        else:
            self._status = 0
            self.visible = 1
            field.checkship(self.shipname)

    def print(self):
        if self.visible == 1:
            return "#" if self._status == 1 else '*'
        else:
            return "~" if self._status == 1 else '*'


class Ship:
    def __init__(self, x, y, orient, size, field, visible):
        self.x = x
        self.y = y
        self.orient = orient
        self.size = size
        self.field = field
        if orient == 1:
            #TODO Нужно написать скрипт проверки занятости по всем точкам, в которые поставим корабль!
            for l in range(size):
                field.setdot(x,y+l,Deck(x,y+l,self, visible), self)
        else:
            for l in range(size):
                field.setdot(x+l,y,Deck(x+l,y,self, visible), self)
        for b in [j.coord() for j in self.field.shipdict.get(self)]:
            i,j = b
            round = [(1,0),(-1,0),(1,1),(0,1),(0,-1),(-1,1),(-1,-1),(1,-1)]
            for di,dj in round:
                try:
                    self.field.occupy(i+di, j+dj)
                except (BoardUsedException, IndexError) as e:
                    continue
    def contour(self):
        for b in [j.coord() for j in self.field.shipdict.get(self)]:
            i,j = b
            round = [(1,0),(-1,0),(1,1),(0,1),(0,-1),(-1,1),(-1,-1),(1,-1)]
            for di,dj in round:
                try:
                    self.field.shoot(i+di, j+dj)
                except (BoardUsedException, IndexError) as e:
                    continue



# Создание корабля помещает его имя в дочернние точки и словарь кораблей в игровом поле. При попадании в точку метод запускает проверку остатка живых точек в корабле.
# Если точки в корабле остались кричим, что ранили. Если нет, убили, и запскаем процесс оконтуривания.

class Field:
    def __init__(self, boardsize):
        self.sea = array([[Dot(i, j) for i in range(boardsize)] for j in range(boardsize)])
        self.shipdict = dict()
        self.kills = 0
    @property
    def lookup(self):
        return self.sea
    def display(self):
        print('       1   2   3   4   5   6')
        print('----------------------------')
        for i in range(6):
            print(i + 1, ' | ', *[f' {x.print()} ' for x in self.lookup[i]])
    def shoot(self, x, y):
        self.sea[x, y].shot(self)
    def occupy(self, x, y):
        self.sea[x, y].occupy()
    def shipdict(self):
        return self.shipdict()
    @property
    def killcount(self):
        return self.kills
    def checkship(self, shipname):
        _ = [i.status for i in self.shipdict.get(shipname)]
        if 1 in _:
            print('Корабль ранен!')
        else:
            print(f'Вы уничтожили корабль!')
            self.kills += 1
            shipname.contour()
    def setdot(self, x, y, obj, shipname):
        if self.sea[x,y].occ_state == 1:
            raise WrongShipSetting()
        else:
            self.sea[x, y] = obj
            if self.shipdict.get(shipname):
                self.shipdict[shipname].append(obj)
            else:
                d1 = {shipname:[obj]}
                self.shipdict.update(d1)

class Game():
    def __init__(self, boardsize = 6):
        self.boardsize = boardsize
        humanboard = self.r_field()
        benderboard = self.r_field(0)


        self.bender = AI(benderboard, humanboard)
        self.human = User(humanboard, benderboard)

    def r_field(self, visible = 1):
        shipsizes = [ 3, 2, 2, 1, 1, 1, 1]
        field = Field(self.boardsize)
        for i in shipsizes:
            while True:
                try:
                    ship = Ship(randint(0, self.boardsize), randint(0, self.boardsize), randint(1, 2), i, field, visible)
                    break
                except (BoardUsedException, IndexError, WrongShipSetting) as e:
                    pass
        return field
    def firstsight(self):
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('~~        Добро пожаловать в игру        ~~')
        print('~~~~~~~~~~~~    Морской Бой!   ~~~~~~~~~~~~')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    def main(self):
        turn = 0
        while True:
            print('~'*20)
            print("               Доска игрока ")
            print(self.humanboard.display())
            print("               Доска адмирала Бендера ")
            print(self.benderboard.display())
            if turn % 2 == 0:
                print(' Ход игрока:')
                self.human.move()
            else:
                print(' Ход Адмирала Бендера:')
                self.bender.move()
            if self.humanboard.killcont == 7:
                print('~'*20)
                print(' Человек одолел! ')
                break
            elif self.benderboard.killcount == 7:
                print('~' * 20)
                print(' Адмирал убил всех человеков! ')
                break
            turn += 1
    def start(self):
        self.firstsight()
        self.main()

g = Game()
g.start()