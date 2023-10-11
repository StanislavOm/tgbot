
import telebot
from tk import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

class ConvertionException(Exception):
    pass


@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'введите команду в следующем формате:\n<имя валюты> \<в какую валюту перевести> \
<количество валюты>\nУвидеть список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(massege: telebot.types.Message):
    text = 'доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(massege, text)


@bot.message_handler(content_types=['text', ])
def convert(massege: telebot.types.Message):
    try:
        values = massege.text.split(' ')
        if len(values) !=3:
            raise ConvertionException('Слишком много параметров')
        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(massege, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
    bot.send_message(massege.chat.id, text)


bot.polling()