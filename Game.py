import random


class Game:

    __id_all            = 0            # статическое поле для id
    __games_list        = dir()        # словарь созданных игр
    __attempts_max      = 5            # максимальное кол-во попыток
    # возможные состояния:
    __game_not_start    = 0            # игра не начата
    __game_start        = 1            # игра начата
    __game_win          = 2            # игра выиграна
    __game_lose         = 3            # игра проиграна
    __game_status_list = {             # словарь статусов игры
            __game_not_start: 'Игра не начата',
            __game_start: 'Игры идет',
            __game_win: 'Игра выиграна',
            __game_lose: 'Игра проиграна'
    }
    __value_max = 99
    __value_min = 0

    def __init__(self):
       self.__attempts_current = 0                       # кол-во сделанных попыток
       self.__secret_value = 0                           # загаданное число
       self.__last_attempt = 0                           # последняя попытка пользователя
       self.__game_status = 0                            # статус игры
       self.__game_id = Game.__id_all                    # id игры
       Game.__id_all = Game.__id_all + 1
       Game.__games_list[self.__game_id] = self          # сохраняем игру в словарь

    # ---------------------Свойства-----------------------
    @property
    def value_max(self):
        return Game.__value_max

    @property
    def value_min(self):
        return Game.__value_min

    @property
    def attempts_current(self):
        return self.__attempts_current

    @property
    def attempts_max(self):
        return Game.__attempts_max

    @property
    def game_id(self):
        return self.__game_id

    # возвращает символьное обозначение статуса
    @property
    def game_status(self):
        return Game.__game_status_list[self.__games]

    # возвращает id статуса
    @property
    def _game_status(self):
        return self.__game_status

    @property
    def get_possible_statuses_game(self):
        # возвращаем строку всех возможных статусов игры
        status_list = list()
        for key in Game.__game_status_list:
            status_list.append(str(key) + ' - ' + Game.__game_status_list[key] + ';')
        return ' '.join(status_list)

    # получение доступных попыток
    @property
    def number_available_attempts(self):
        return Game.__attempts_max - self.__attempts_current

    # возвращает разность между загаданным числом и последним ответом
    @property
    def _delta_answer(self):
        return self.__secret_value - self.__last_attempt

    @property
    def get_game_status_list(self):
        return Game.__game_status_list

    @property
    def _secret_value(self):
        return self.__secret_value

    @property
    def _game_not_start(self):
        return Game.__game_not_start

    @property
    def _game_start(self):
        return Game.__game_start

    @property
    def _game_win(self):
        return  Game.__game_win

    @property
    def _game_lose(self):
        return Game.__game_lose
    # ---------------------Методы-----------------------



    # начать игру
    def start_game(self):
        self.__secret_value = random.randint(0, 99)
        self.__game_status = 1

    # сделать попытку по угадыванию числа
    def make_attempt(self, value):
        self.__last_attempt = value                                 # обновляем значение крайней попытки
        self.__attempts_current = self.__attempts_current + 1       # обновляем кол-во попыток
        return self._check_answer()

    def _check_answer(self):
        # если игра уже выиграна
        if self.__game_status == Game.__game_win:
            return True
        # если игра проиграна или не начата или кол-во попыток израсходовано
        if self.__game_status == Game.__game_lose or self.__game_status == Game.__game_not_start \
                or self.__attempts_current > Game.__attempts_max:
            return False

        # если число было угадано
        if self.__last_attempt == self.__secret_value:
            self.__game_status = Game.__game_win
            return True

        if self.number_available_attempts == 0:
            self.__game_status = Game.__game_lose

        return False
    # ---------------------Конец класса-----------------------