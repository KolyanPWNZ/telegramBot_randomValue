# ссылка на бота @CodemikaRandomValueNik

import config
import telebot
import random

bot = telebot.TeleBot(config.telegram_token)

class Game:
    __id_all = 0                # статическое поле для id
    __games_list = dir()        # словарь созданных игр
    __attempts_max = 5            # максимальное кол-во попыток
    __game_status_list = {      # словарь статусов игры
        0: 'Игра не начата',
        1: 'Игры идет',
        2: 'Игра выиграна',
        3: 'Игра проиграна'
    }

    def __init__(self):
       self.__attempts_current = 0                       # кол-во сделанных попыток
       self.__secret_value = 0                           # загаданное число
       self.__last_attempt = 0                           # последняя попытка пользователя
       self.__game_id = Game.__id_all                    # id игры
       self.__game_status = 0                            # статус игры
       Game.__id_all = Game.__id_all + 1
       Game.__games_list[self.__game_id] = self          # сохраняем игру в словарь

    #----------------------Свойства-----------------------
    @property
    def attempts_current(self):
        return self.__attempts_current

    @property
    def game_id(self):
        return self.__game_id

    @property
    def attempts_current(self):
        return self.__attempts_current

    @property
    def game_status(self):
        return Game.__game_status_list[self.__games]

    @property
    def get_possible_statuses_game(self):
        # возвращаем строку всех возможных статусов игры
        status_list = list()
        for key in Game.__game_status_list:
            status_list.append(str(key) + ' - ' + Game.__game_status_list[key] + ';')
        return ' '.join(status_list)

    # ---------------------Методы-----------------------
    # начать игру
    def start_game(self):
        self.__secret_value = random.randint(0, 99)
        self.__game_status = 1

    # сделать попытку по угадыванию числа
    def make_attempt(self, value):
        self.__last_attempt = value                                 # обновляем значение крайней попытки

        if value == self.__secret_value and self.__game_status == 1 and self.__attempts_current() <= Game.__attempts_max:
            self.__game_status = 2                                  # фиксируем победу
            return True
        else:
            return False

    # # # обновление статуса игры
    # def _update_game_status(self):
    #     if self.__last_attempt == self.__secret_value :            # если число было угадано
    #         self.__attempts_current = self.__attempts_current + 1  # обновляем кол-во попыток
    #         self.__






game = None


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, друг! Я хочу сыграть с тобой в одну игру…')
    bot.send_message(message.chat.id, 'Начнем?')

@bot.message_handler(commands=['rules'])
def start(message):
    bot.send_message(message.chat.id, 'Правила игры:'
                                      'Я загадываю число от 0 до 99. А тебе надо '
                                      'отгадать его за ' + str(config.attempts_max) + ' попыток.'
                                      'Если отгадаешь, то будешь большим молодцом, а иначе... '
                                      'я сделаю тебе ничего, потому что я бот (^_^)')

@bot.message_handler(commands=['start game'])
def start(message):
    bot.send_message(message.chat.id, 'А ты смельчак! Ну что ж, начнем игру!')






bot.polling(none_stop=True)