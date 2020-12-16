import telebot
from datetime import date, timedelta
import requests
import json
import types


api_key = 'https://stepik.akentev.com/api/weather'
token = '1426279811:AAHp669I2dr-8V-5PBivmqibb5bdVrKgeLk'
bot = telebot.TeleBot(token)

try:
    data = json.load(open('db/data.json', 'r', encoding = 'utf-8'))
except FileNotFoundError:
    data = {
        'states': {},
        MAIN_STATE: {
        },
        CITY_STATE: {
        },
        WEATHER_DATE_STATE: {
        },
    }

MAIN_STATE = 'main'
WEATHER_DATE_STATE = 'weather_date_handler'
CITY_STATE = 'city'


def change_data(key, user_id, value):
    data[key][user_id] = value
    json.dump(
        data,
        open('db/data.json', 'w', encoding='utf-8'),
        indent=2,
        ensure_ascii=False,
    )


@bot.message_handler(func = lambda message: True)
def dispatcher(message):
    user_id = str(message.from_user.id)
    state = data['states'].get(user_id, MAIN_STATE)

    if state == MAIN_STATE:
        main_handler(message)
    elif state == CITY_STATE:
        city_handler(message)
    elif state == WEATHER_DATE_STATE:
        weather_date(message)

def main_handler(message):
    user_id = str(message.from_user.id)
    if message.text == '/start':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Погода'))
        bot.send_message(
             user.id,
            'Привет! Это бот-погода, который поможет тебе узнать погоду в любом городе.',
            reply_markup=markup,
        )
        change_data('states',user_id, MAIN_STATE)


    elif message.text == 'Погода':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        murkup.add(
            *[types.KeyboardButton(button) for button in ['Москва', 'Санкт-Петербург']]
        )
        bot.send_message(user_id, 'Какой город интересует? Москва или Спб?', reply_markup=markup)
        change_data('states',user_id, CITY_STATE)

    else:
        markup = types.ReplyKeybordRemove()
        bot.send_message(user_id, 'Я тебя не понял', reply_markup=markup)



def city_handler(message):
    user_id = str(message.from_user.id)
    if message.text.lower() in ['Москва', 'Санкт-Петербург']:
        change_data(WEATHER_DATE_STATE,user_id, message.text.lower())
        markup = types.ReplyKeyBoardMarkup(resize_keyboard = True, one_time_keyboard=True)
        murkup.add(
            *[types.KeyboardButton(button) for button in ['Сегодня','Завтра']]
        )
        bot.send_message(user_id, 'Какая дата интересует? Сегодня или завтра?', reply_markup=markup)
        change_data('states', user_id, WEATHER_DATE_STATE )
    else:
        bot.reply_to(message, 'Я тебя не понял')

WEATHER = {
    'Санкт-Петербург': {
        'Сегодня': '-10',
        'Завтра': '-15',
    },
    'Москва': {
        'Сегодня': '-5',
        'Завтра': '2',
    }
}

def weather_date(message):
    user_id = str(message.from_user.id)
    city = data[WEATHER_DATE_STATE][user_id]

    if message.text == 'Сегодня':
        bot.send_message(user_id, WEATHER[city][message.text.lower()])
        change_data('states', user_id, MAIN_STATE)

    elif message.text == 'Завтра':
        bot.send_message(user_id, WEATHER[city][message.text.lower()])
        change_data('states', user_id, MAIN_STATE)

    else:
        bot.reply_to(message, 'Я тебя не понял')

if __name__ == '__main__':
    bot.polling()

