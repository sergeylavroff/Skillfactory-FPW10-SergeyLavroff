from numpy import array
from random import randint
class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __repr__(self):
        return "Выстрел за пределы доски!"

class BoardUsedException(BoardException):
    def __repr__(self):
        return "Точка уже поражена!"

class WrongShipSetting(BoardException):
    def __str__(self):
        return "Корабль не может быть размещен в заданной точке!"
# Класс точка, базовый класс.
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

# Объект палуба аналогичен точке, но имеет параметр видимости для реализации вражеского поля.
# При попадании запускает метод проверки оставшихся палуб объекта корабль.
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
# При иничиализации объекта корабля происходит проверка возможности установки в заданные точки,
# собственно создание точек и отметка прилегающих точек как занятых.
    def __init__(self, x, y, orient, size, field, visible):
        self.x = x
        self.y = y
        self.orient = orient
        self.size = size
        self.field = field
        if orient == 1:
            for l in range(size):
                if y+l > 6:
                    raise WrongShipSetting
                if field.check_occ(x, y + l) == 1:
                    raise WrongShipSetting
            for l in range(size):
                field.setdot(x,y+l,Deck(x,y+l,self, visible), self)
        else:
            for l in range(size):
                if x+l > 6:
                    raise WrongShipSetting
                if field.check_occ(x + l, y) == 1:
                    raise WrongShipSetting
            for l in range(size):
                field.setdot(x+l,y,Deck(x+l,y,self, visible), self)
        for b in [j.coord() for j in self.field.shipdict.get(self)]:
            i,j = b
            round = [(1,0),(-1,0),(1,1),(0,1),(0,-1),(-1,1),(-1,-1),(1,-1)]
            for di,dj in round:
                try:
                    if 0 > (i + di) or (i + di) >= self.field.boardsize or 0 > (j + dj) or (j + dj) >= self.field.boardsize:
                        raise BoardUsedException
                    self.field.occupy(i+di, j+dj)
                except (BoardUsedException) as e:
                    continue
#Процедура оконтуривания уничтоженного корабля
    def contour(self):
        for b in [j.coord() for j in self.field.shipdict.get(self)]:
            i,j = b
            round = [(1,0),(-1,0),(1,1),(0,1),(0,-1),(-1,1),(-1,-1),(1,-1)]
            for di,dj in round:
                try:
                    if 0 > (i + di) or (i + di) >= self.field.boardsize or 0 > (j + dj) or (j + dj) >= self.field.boardsize:
                        raise BoardUsedException
                    self.field.shoot(i+di, j+dj)
                except BoardUsedException:
                    continue



# Создание корабля помещает его имя в дочернние точки и словарь кораблей в игровом поле. При попадании в точку метод запускает проверку остатка живых точек в корабле.
# Если точки в корабле остались кричим, что ранили. Если нет, убили, и запскаем процесс оконтуривания.

class Field:
    def __init__(self, boardsize):
        self.sea = array([[Dot(i, j) for i in range(boardsize)] for j in range(boardsize)])
        self.shipdict = dict()
        self.kills = 0
        self.boardsize = boardsize
    @property
    def lookup(self):
        return self.sea
    def check_occ(self, x, y):
        return self.sea[x, y].occ_state
    def display(self, i):
        a = (str(i + 1), ' | ', *[f' {x.print()} ' for x in self.lookup[i]])
        return ''.join(a)
    def shoot(self, x, y):
        self.sea[x, y].shot(self)
    def occupy(self, x, y):
        self.sea[x, y].occupy()
    def shipdict(self):
        return self.shipdict()
    @property
    def killcount(self):
        return self.kills
# Проверка остатка живых палуб корабля, в случае отсутствия таковых запускаем оконтуривание точками.
    def checkship(self, shipname):
        _ = [i.status for i in self.shipdict.get(shipname)]
        if 1 in _:
            print('Корабль ранен!')
        else:
            print(f'Вы уничтожили корабль!')
            self.kills += 1
            shipname.contour()
# Установка точек корабля на игровое поле
    def setdot(self, x, y, obj, shipname):
        self.sea[x, y] = obj
        if self.shipdict.get(shipname):
            self.shipdict[shipname].append(obj)
        else:
            d1 = {shipname:[obj]}
            self.shipdict.update(d1)

class Player:
    def __init__(self, myfield, oppfield, boardsize = 6):
        self.myfield = myfield
        self.oppfield = oppfield
        self.boardsize = boardsize

class Bender(Player):
    def move(self):
        x = 0
        y = 0
        while True:
            try:
                x = randint(0,self.boardsize-1)
                y = randint(0, self.boardsize-1)
                self.oppfield.shoot(x, y)
                print(f" Армада Адмирала Бендера ударила по точке {y + 1},{x + 1}!")
                break
            except BoardUsedException:
                continue

class Human(Player):
    def move(self):
        print(" Господин Адмирал! Вам нужно указать точку удара!")
        while True:
            y = input(" Введите номер столбца:")
            x = input(" Введите номер строки:")
            if not(y.isdigit()) or not(x.isdigit()):
                print("Адмирал, это даже не числа, наш флот под обстрелом, соберитесь!")
                continue
            y = int(y)
            x = int(x)
            if not(y in range(1, self.boardsize + 1)) or not(x in range(1, self.boardsize + 1)):
                print(f"Адмирал, враг сосредоточен в точках от 0 до {self.boardsize}!) ")
                continue
            try:
                self.oppfield.shoot(x-1, y-1)
                break
            except BoardUsedException:
                print("Эта точка уже поражена!")
                continue

class Game():
    def __init__(self, boardsize = 6):
        self.boardsize = boardsize
        self.humanboard = self.get_field()
        self.benderboard = self.get_field(0)
        self.bender = Bender(self.benderboard, self.humanboard)
        self.human = Human(self.humanboard, self.benderboard)
# Создание случайного поля:
    def get_field(self, visible = 1):
        field = None
        while field is None:
            field = self.r_field(visible)
        return field

    def r_field(self, visible=1):
        shipsizes = [3, 2, 2, 1, 1, 1, 1]
        field = Field(self.boardsize)
        counter = 0
        for i in shipsizes:
            while True:
                if counter > 1000:
                    return None
                try:
                    ship = Ship(randint(0, self.boardsize), randint(0, self.boardsize), randint(1, 2), i, field, visible)
                    break
                except (BoardUsedException, IndexError, WrongShipSetting) as e:
                    counter += 1
                    pass
        return field

    def firstsight(self):
        print('           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('           ~~        Добро пожаловать в игру        ~~')
        print('           ~~~~~~~~~~~~    Морской Бой!   ~~~~~~~~~~~~')
        print('           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    def simultaneous_disp(self):
        print(f"      Доска игрока     {'~~~' * self.boardsize}    Доска Адмирала Бендера")
        print(f"     {'| '.join([str(i+1) for i in range(self.boardsize)])}                       "*2)
        print('___________'*self.boardsize)
        for i in range(self.boardsize):
            print(f"{self.humanboard.display(i)}  {'~~~' * self.boardsize}  {self.benderboard.display(i)}")
    def main(self):
        turn = 0
        while True:
            self.simultaneous_disp()
            if turn % 2 == 0:
                print(' Ход игрока:')
                self.human.move()
            else:
                print(' Ход Адмирала Бендера:')
                self.bender.move()
            if self.benderboard.killcount == 7:
                print('~'*20)
                print(' Суда подконтрольные сумасшедшему ИИ уничтожены, Адмирал! ')
                break
            elif self.humanboard.killcount == 7:
                print('~' * 20)
                print(' Адмирал Бендер убил всех человеков! ')
                break
            turn += 1
    def start(self):
        self.firstsight()
        self.main()

g = Game()
g.start()
