from random import randrange
from termcolor import colored
from os import system


class Cell:
    def __init__(self, around_mines=0, mine=False):
        self.around_mines = around_mines
        self.mine = mine
        self.fl_open = False
        self.demined = False


class GamePole:
    def __init__(self, N, M):
        self.N = N  # размерность поля N*N
        self.M = M  # фиксированное изначальное положение мин
        self.pole = [[Cell() for _ in range(self.N)] for _ in range(self.N)]  # вложенный список экземпляров класса Cell
        self.health = 3
        self.create_table()

    def create_table(self):
        '''Функция заполняет случайные ячейки минами, и присваивает другим ячейкам значения о минах вокруг'''
        m = 0
        while m < self.M:
            i = randrange(0, self.N)
            j = randrange(0, self.N)
            if self.pole[i][j].mine == True:
                continue
            else:
                self.pole[i][j].mine = True
                m += 1

        indx = (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)
        for x in range(self.N):
            for y in range(self.N):
                if self.pole[x][y].mine == False:
                    mines = sum(
                        (self.pole[x + i][y + j].mine for i, j in indx if 0 <= x + i < self.N and 0 <= y + j < self.N))
                    self.pole[x][y].around_mines = mines

    def open_cell(self):
        '''функция передаёт в метод .fl_open значение True, для открытой ячейки и путсых ячеек вокруг'''
        indx = (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)
        for x, y in indx:
            if self.pole[self.row][self.column].mine == False:
                if 0 <= x + self.row < self.N and \
                        0 <= y + self.column < self.N and \
                        self.pole[x + self.row][y + self.column].mine == False:
                    self.pole[x + self.row][y + self.column].fl_open = True

    def try_demining(self):
        '''в функции реализована логика разминирования'''
        if self.pole[self.row][self.column].mine == True and self.pole[self.row][self.column].demined == False:
            self.pole[self.row][self.column].demined = True
            self.demined_count -= 1
            print(f'Мина успешно разминированна! Осталось {self.demined_count}')
        elif self.pole[self.row][self.column].mine == True and self.pole[self.row][self.column].demined == True:
            print('Эта мина уже разминированна')
        else:
            self.health -= 1
            print(f'Вы ошиблись! У вас осталось {self.health} жизни')
        if self.health == 0:
            print('К сожалению, вы проиграли')
            self.regame()

    def show(self):
        '''функция отрисовывает игровое поле после каждого хода'''
        print('   ', end='')
        str(print(*range(1, self.N+1), sep='|'))
        for count, row in enumerate(self.pole, start=1):
            print(f'{count}| ' if count < 10 else f'{count}|', end='')
            print(*map(
                lambda x: colored('#', 'green') if not x.fl_open else x.around_mines \
                    if not x.mine else colored('*', ('red', 'yellow')[x.demined]), row))
        print('-' * 22)

    def regame(self):
        '''функция рестарта игры при победе/проигрыше'''
        print('Хотите сыграть ещё раз? да/нет')
        if input() in ['да', 'ДА', 'Да', 'lf', 'Lf', 'LF']:
            new_pole_game = GamePole(self.N, self.M)
            system('cls')
            new_pole_game.play()
        else:
            input('Спасибо за игру!!! Нажмите Enter, чтобы выйти')
            exit()

    def lose_checker(self):
        '''проверка на проигрыш после каждого хода'''
        if self.pole[self.row][self.column].mine == True and self.pole[self.row][self.column].demined == False:
            print('Вы взорвались!')
            self.regame()

    def win(self):
        '''сообщение о победе, по достижению нуля активных мин'''
        if self.demined_count == 0:
            print('Урааааа!!! Вы победили!!!')
            self.regame()
    def settings(self):
        '''Пока в тестовом режиме, дополнить функционал'''
        print('Вы можете настроить размерность поля, и колличество мин')
        print('Введите два числа через пробел: Размерность поля n*n, и количество мин')
        while True:
            try:
                self.N, self.M = map(int, input().split())
            except:
                print('Введите два значения: размерность поля, и количество мин')
                continue
            self.regame()


    def get_coord(self, row: int, column: int = -1, demine: str = False) -> int:
        '''Input координат пользователя'''
        if row == 'settings':
            self.settings()
        self.row = int(row)
        self.column = int(column)
        while not (0 < self.row <= self.N) or not (0 < self.column <= self.N):
            print(f'Введите координаты от 1 до {self.N}!')
            self.row, self.column = map(int, input().split())
        self.demine = demine
        if demine:
            self.demine = True
        return self.row, self.column

    def play(self):

        print('Приветствую в игре Сапёр!')
        print(f'На поле {self.N} на {self.N} расставлено {self.M} мин. Ваша задача обезвредить их!')
        print()
        print('Чтобы открыть ячейку - введите через пробел два числа: ряд и столбец')
        print('Если вы решите разминировать ячейку - допишите к числам через пробел любое слово. Приступим!!!')
        self.demined_count = self.M
        while self.demined_count:  # пока счётчик мин не равен 0
            try:
                row, column = self.get_coord(*input().split())
            except:
                print(f'Введите два значения от 1 до {self.N}, через пробел')
                continue
            self.row = row - 1
            self.column = column - 1
            self.pole[self.row][self.column].fl_open = True
            if self.demine:
                self.try_demining()  # функция попытки разминирования при передаче 3го аргумента
            self.open_cell()  # функция открытия ячейки и ячеек вокруг неё
            self.show()  # отображаем
            self.lose_checker()  # проверка на проигрыш
        self.win()  # инициализация победы


pole_game = GamePole(10, 12)
pole_game.play()
