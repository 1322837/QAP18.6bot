import telebot
from config import TOKEN, values
from classfile import APIException, Converter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_info(message: telebot.types.Message):
    text = "Чтобы начать работу введите команду в следующем формате:\n <имя валюты цену которой вы хотите узнать>" \
           "<имя валюты в которой надо узнать цену первой валюты><количество первой валюты>" \
           "\nЧто бы получить информацию о доступной валюте ввидите команду /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def send_values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in values.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        message_values = message.text.split(' ')
        for i in range(len(message_values)):
            message_values[i] = message_values[i].lower()

        if len(message_values) != 3:
            raise APIException('Введено неверное количество параметров.')

        quote, base, amount = message_values
        final_value = Converter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        bot.reply_to(message, f"{amount} {quote} будет стоить {final_value} {base}")


bot.polling(none_stop=True)
