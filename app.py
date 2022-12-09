import telebot
import extensions

from config import TOKEN, val, symbols

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def hello(message: telebot.types.Message):
    bot.reply_to(message, 'Привет, чтобы начать работать с ботом нужно ввести команду следующего вида:\n\
<Название валюты> <В какую валюту хотите перевести> <Количество переводимой валюты>\n\
Увидеть все доступные валюты: /values\n\
Десятичные дроби вводятся через точку.')

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for k in val.keys():
        text += f'\n{k}'
    bot.reply_to(message, text)

@bot.message_handler()
def convert(message: telebot.types.Message):
    message_args = message.text.split()
    try:
        if len(message_args)!=3:
            raise extensions.WrongMessageException
        base, quote, amount = message_args
        extensions.ExceptionAnalyzer.exception_check(base, quote, amount)
    except Exception as e:
        bot.reply_to(message, f'Ошибка пользователя. {e}')
    else:
        base_ticker, quote_ticker = val[base], val[quote]
        result = extensions.RequestAPI.get_price(base_ticker, quote_ticker, amount)
        bot.reply_to(message, f'Цена {amount}{symbols[base_ticker]} в {quote} - '+str(result)+symbols[quote_ticker])
    
bot.polling(none_stop=True)
