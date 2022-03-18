# ссылка на бота @CodemikaRandomValueNik

import config
import telebot
from Game import Game

bot = telebot.TeleBot(config.telegram_token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, друг! Я хочу сыграть с тобой в одну игру…')
    bot.send_message(message.chat.id, 'Начнем?')
    config.game = Game()                    # создаем игру


@bot.message_handler(commands=['rules'])
def start(message):
    bot.send_message(message.chat.id, 'Правила игры:'
                                      'Я загадываю число от 0 до 99. А тебе надо '
                                      'отгадать его за ' + str(config.attempts_max) + ' попыток.'
                                      'Если отгадаешь, то будешь большим молодцом, а иначе... '
                                      'я сделаю тебе ничего, потому что я бот (^_^)')

@bot.message_handler(commands=['start game'])
def start(message):
    if config.game is None:
        config.game = Game()
    config.game.start_game()
    bot.send_message(message.chat.id, 'А ты смельчак! Ну что ж, начнем игру!')
    bot.send_message(message.chat.id, 'Я загадал число от 0 до 99. Жду от тебя ответа.')
    bot.send_message(message.chat.id, 'Даю тебе ' + str(config.game.number_available_attempts) + ' попыток')


@bot.message_handler(content_types=['text'])
def text(message):
    if type(message.text) != int:
        bot.send_message(message.chat.id, 'Наверно стоит попробовать ввести число...')
        bot.send_message(message.chat.id, 'Так уж и быть попытку забирать не буду')
        return

    answer = int(message.text)

    if config.game.make_attempt():
        attempt_cur = config.game.attempts_current # получили кол-во доступных попыток
        if attempt_cur == 1:
            bot.send_message(message.chat.id, 'Ого! Так легко отделались... Везение? Или суровый расчет? '
                                              'В любом случае поздравляю! Вы молодец!')
        elif attempt_cur == 2:
            bot.send_message(message.chat.id, 'Эх, зря подсказывал! Так бы еще поиграли. Поздравляю! Вы победили!')
        elif attempt_cur == 3:
            bot.send_message(message.chat.id, 'Неплохо сыграно! Поздравляю Вас с победой!')
        elif attempt_cur == 4:
            bot.send_message(message.chat.id, 'Еще чуть-чуть и я бы победил :( \nВы молодец, поздравляю вас!')
        elif attempt_cur == 5:
            bot.send_message(message.chat.id, 'На грани! Думал, что Вы уже не победите! Но Вы справились и собрались в последний момент!'
                                              '\nПоздравляю Вас с победой!')


    if int(message.text) > config.game.value_max or int(message.text) < config.game.value_min:
        bot.send_message(message.chat.id, 'Хм, ответ интересный... Наверное, стоит попробовать вводить числа в заданном диапазоне =) \n'
                                          'Может быть так получится угадать?')




bot.polling(none_stop=True)