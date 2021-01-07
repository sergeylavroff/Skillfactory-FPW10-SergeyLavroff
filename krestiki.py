from numpy import array, diagonal, fliplr

print("Привет, давай сыграем в крестики-нолики")

name1 = input("Введите имя первого игрока:")
name2 = input("Введите имя второго игрока:")
game = array([[' ', 1, 2, 3], [1, "-", "-", "-"], [2, "-", "-", "-"], [3, "-", "-", "-"]])


def print_field(game=game):
    for i in game:
        print(*i)


print("Игровое поле:")
print_field(game)


def put_sign(name, sign):
    appropriate = [1, 2, 3]
    if name == name1:
        coord = input(f'Игрок {name} введите координаты куда поставим крестик:')
    else:
        coord = input(f'Игрок {name} введите координаты куда поставим нолик:')
    if len(coord) == 2 and int(coord[0]) in appropriate and int(coord[1]) in appropriate:
        if game[int(coord[0])][int(coord[1])] == '-':
            game[int(coord[0])][int(coord[1])] = sign
            print_field()
        else:
            print('Здесь уже есть что то, зачем Вы так?')
            put_sign(name, sign)
    else:
        print("Формат введенных координат не соответствует игровому полю, попробуйте снова!")
        put_sign(name, sign)


def winner(game=game):
    for i in game:
        if len(set(i[1:])) == 1:
            if i[1] == 'x':
                return name1
            elif i[1] == 'o':
                return name2
    for j in range(1, 4):
        if len(set(game[1:, j])) == 1:
            if game[1, j] == 'x':
                return name1
            elif game[1, j] == 'o':
                return name2
    if len(set(game[1:, 1:].diagonal())) == 1:
        if game[1, 1] == 'x':
            return name1
        elif game[1, 1] == 'o':
            return name2
    if len(set(fliplr(game[1:, 1:]).diagonal())) == 1:
        if game[3, 3] == 'x' and game[2, 2] == 'x':
            return name1
        elif game[3, 3] == 'o' and game[2, 2] == 'o':
            return name2


def main():
    round = 1
    print(f"Да начнется битва, раунд {round}!")
    print("Для ввода координат введите две цифры без пробелов. "
          "Например, 11 чтобы поставить крестик в первую строчку и первую колонку.")
    while True:
        if round != 1:
            print(f"Продолжим, раунд {round}!")
        # Ход крестика
        put_sign(name1, 'x')
        if winner(game):
            print("Победитель", winner(game))
            break
        if round == 5:
            print("Ничья!")
            break
        put_sign(name2, 'o')
        if winner(game):
            print("Победитель", winner(game))
            break
        round += 1


main()
