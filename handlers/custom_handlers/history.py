from config_data.pathes_data import history_path
import time
from loader import bot
import sqlite3
from telebot.types import Message
import os
from typing import List
from handlers.custom_handlers import survey
from handlers.default_heandlers import help, start


@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    """
    The function-handler, which gets all items from history.db
    and sends them to the user.

    :param message: This is a message from the user
    :type message: Message
    """
    if os.path.exists(history_path):
        with sqlite3.connect(r'{}'.format(history_path)) as database:
            cur = database.cursor()
            cur.execute("SELECT * FROM history WHERE userid='{}'".format(message.from_user.id))
            result: List[str] = cur.fetchall()
            if len(result) != 0:
                bot.send_message(message.from_user.id, 'Вот ваша история поиска')
                for i_request in result:
                    text = 'Ссылка: {url}\n' \
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
    else:
        bot.send_message(message.from_user.id, 'Ваша история поиска пуста, самое время это исправить :)')

    bot.set_state(message.from_user.id, None, message.chat.id)