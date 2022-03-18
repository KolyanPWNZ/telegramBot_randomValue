# ссылка на бота @CodemikaRandomValueNik

import config
import telebot
from Game import Game

bot = telebot.TeleBot(config.telegram_token)


# функция начальной настройки игры
def check_game(chat_id) -> bool:
    if config.game is None or config.game._game_status != config.game._game_start:
        bot.send_message(chat_id, 'Внимание: необходимо пересоздать игру!')
        return False
    else:
        return True


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, друг! Я хочу сыграть с тобой в одну игру…')
    bot.send_message(message.chat.id, 'Начнем?')


@bot.message_handler(commands=['rules'])
def rules(message):
    if not check_game(message.chat.id):
        return

    bot.send_message(message.chat.id, 'Правила игры:\n'
                                      'Я загадываю число от ' + str(config.game.value_min) + ' до ' + str(config.game.value_max) + '. '
                                      ' А тебе надо отгадать его за ' + str(config.game.attempts_max) + ' попыток.'
                                      '\nЕсли отгадаешь - будешь большим молодцом, а иначе... '
                                      'я сделаю тебе ничего, потому что я бот (^_^)')

@bot.message_handler(commands=['game'])
def start(message):
    config.game = Game()
    config.game.start_game()
    bot.send_message(message.chat.id, 'А ты смельчак! Ну что ж, начнем игру!')
    bot.send_message(message.chat.id, 'Я загадал число от' + str(config.game.value_min) + ' до ' + str(config.game.value_max) + '.'
                    'Жду от тебя ответа.')
    bot.send_message(message.chat.id, 'Даю Вам ' + str(config.game.number_available_attempts) + ' попыток')


@bot.message_handler(content_types=['text'])
def text(message):
    if not check_game(message.chat.id):                 # проверяем, что игра создана
        return

    if config.game.number_available_attempts == 0:      # проверяем что еще можем играть
        bot.send_message(message.chat.id, 'Если захотите еще поиграть то запускайте игру заново')

    if not message.text.isdigit():                      # проверка что входное число можно преобразовать в число
        bot.send_message(message.chat.id, 'Наверно стоит попробовать ввести число...')
        bot.send_message(message.chat.id, 'Так уж и быть, попытку забирать не буду')
        return

    answer = int(message.text)                          # фиксируем ответ
    if config.game.make_attempt(answer):                # проверяем ответ

        # в случае правильного ответа
        attempt_cur = config.game.attempts_current      # получили кол-во доступных попыток
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
    else:
        if answer > config.game.value_max or answer < config.game.value_min:
            bot.send_message(message.chat.id, 'Хм, ответ интересный... Наверное, стоит попробовать вводить числа в заданном диапазоне =) \n'
                                              'Может быть так получится угадать?')
        else:
            if config.game.number_available_attempts > 0:
                bot.send_message(message.chat.id, 'Осталось - ' + str(config.game.number_available_attempts) + ' попыток')
            else:
                bot.send_message(message.chat.id, 'К сожалению вы проиграли :(')
                bot.send_message(message.chat.id, 'Правильный ответ был ' + str(config.game._secret_value))
                bot.send_message(message.chat.id, 'Если захотите еще поиграть, то запускайте игру заново')
                return

            delta = config.game._delta_answer      # получаем разницу между заданным числом и ответом
            # Формируем подсказки пользователю
            if delta >= 40:
                bot.send_message(message.chat.id, 'Попробуйте взять число значительно больше')
            elif delta <= -40:
                bot.send_message(message.chat.id, 'Попробуйте взять число значительно меньше')

            elif delta >= 20:
                bot.send_message(message.chat.id, 'Попробуйте взять число побольше!')
            elif delta <= -20 and delta :
                bot.send_message(message.chat.id, 'Попробуйте взять число поменьше!')

            elif delta >= 10:
                bot.send_message(message.chat.id, 'Уже тепло! Я бы на вашем месте попробовал взять чуть больше')
            elif delta <= -10:
                bot.send_message(message.chat.id, 'Уже тепло! Я бы на вашем месте попробовал взять чуть меньше')

            elif delta >= 5:
                bot.send_message(message.chat.id, 'Совсем тепло! Добавьте совсем немного и вы победите!')
            elif delta <= -5:
                bot.send_message(message.chat.id, 'Совсем тепло! Добавьте совсем немного и вы победите!')

            elif delta < 5 or delta > -5:
                bot.send_message(message.chat.id, 'Вы так близко, что я и подсказывать не буду 0_0')


bot.polling(none_stop=True)