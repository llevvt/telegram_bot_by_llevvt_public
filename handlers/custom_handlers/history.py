from config_data.pathes_data import history_path
import time
from loader import bot
import sqlite3
from telebot.types import Message
import os
from handlers.custom_handlers import low, survey


@bot.message_handler(commands=['history'])
def history(message: Message):
    if os.path.exists(history_path):
        bot.send_message(message.from_user.id, 'Вот ваша история поиска')
        with sqlite3.connect(r'{}'.format(history_path)) as database:
            cur = database.cursor()
            cur.execute("SELECT * FROM history WHERE userid='{}'".format(message.from_user.id))
            result = cur.fetchall()
            for i_request in result:
                text = 'ID пользователя: {user_id}\n' \
                       'Ссылка: {url}\n' \
                       'Название отеля: {hotel_name}\n' \
                       'Город: {city}\n' \
                       'Рейтинг: {rating}\n' \
                       'Стоимость: {price}$'.format(
                        user_id=i_request[0],
                        url=i_request[1],
                        hotel_name=i_request[2],
                        city=i_request[3],
                        rating=i_request[4],
                        price=i_request[5]
                        )
                bot.send_message(message.from_user.id, text)
                time.sleep(0.5)
    else:
        bot.send_message(message.from_user.id, 'Ваша история поиска пуста, самое время это исправить :)')