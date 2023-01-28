from config_data.pathes_data import history_path
import time
from loader import bot
import json


@bot.message_handler(commands=['history'])
def history(message):
    with open(history_path, 'r') as file:
        history_data = json.load(file)
        if len(history_data.keys()) == 0:
            bot.send_message(message.from_user.id, 'У Вас пока нет истории поиска')

        else:
            bot.send_message(message.from_user.id, 'Вот ваша история поиска')

            for i_key in history_data.keys():
                current_dict = history_data[i_key]
                text = f'Город: {current_dict["city"]}\n'\
                       f'Название жилья: {current_dict["name"]}\n' \
                       f'Тип жилья: {current_dict["type"]}\n' \
                       f'Рейтинг: {current_dict["rating"]}\n' \
                       f'Стоимость: {current_dict["price"]}$\n' \
                       f'Ссылка: {current_dict["url"]}'
                bot.send_message(message.from_user.id, text)
                time.sleep(1)
