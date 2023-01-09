from loader import bot
from states.request_state import RequestState
from telebot.types import Message
from utils.data_processing.get_data import new_data
from utils.data_processing.processing_data import processing_data
from utils.data_processing.save_request import save_request
from utils.data_processing.sorting_data import sorting_data
from config_data.pathes_data import current_request
import json


@bot.message_handler(commands=['low'])
def get_data(message: Message) -> None:
    bot.set_state(message.from_user.id, RequestState.city, message.chat.id)
    bot.send_message(message.from_user.id, f'Введи город назначения')


@bot.message_handler(state=RequestState.city)
def get_city(message: Message):
    bot.send_message(message.from_user.id, 'Спасибо, записал! Теперь введи дату заезда в формате YYYY-MM-DD')
    bot.set_state(message.from_user.id, RequestState.check_in_date, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text


@bot.message_handler(state=RequestState.check_in_date)
def get_check_in_date(message):
    bot.send_message(message.from_user.id, 'Спасибо, записал! Теперь введи дату выезда в формате YYYY-MM-DD')
    bot.set_state(message.from_user.id, RequestState.check_out_date, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['checkin'] = message.text


@bot.message_handler(state=RequestState.check_out_date)
def get_check_out_day(message):
    bot.send_message(message.from_user.id, 'Спасибо, записал!')

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['checkout'] = message.text

    text = f'Спасибо за предоставленную информацию! Ваши данные:\n' \
           f'Город: {data["city"]}\n' \
           f'Дата въезда: {data["checkin"]}\n' \
           f'Дата выезда: {data["checkout"]}\n'
    bot.send_message(message.from_user.id, text)
    low_offer = get_low(message=message)
    with open(current_request, 'r') as file:
        current_data = json.load(file)
        result = current_data[low_offer]
        text = 'Вот ваш вариант!\n'\
                '\nНазвание: {name}\n'\
                'Ссылка: {link}\n'\
                'Рейтинг: {rating}\n'.format(
                name=result['name'], link=result['url'], rating=result['rating']
    )
        bot.send_message(message.from_user.id, text)


def get_low(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        current_response = new_data(
            location=data['city'], checkin=data['checkin'], checkout=data['checkout']
        )
        processing_data(request_dict=current_response)
        current_response = sorting_data()
        return current_response[0]





