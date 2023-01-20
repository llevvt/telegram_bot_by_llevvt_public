from loader import bot
from states.request_state import RequestState
from telebot.types import Message
from utils.data_processing.get_data import new_data
from utils.data_processing.processing_data import processing_data
from utils.data_processing.save_request import save_request
from utils.data_processing.sorting_data import sorting_data
from config_data.pathes_data import current_request
import json
import re
from utils.other_utils.cheking_date import checking_date
from config_data.request_config import current_date, next_date


@bot.message_handler(commands=['low'])
def get_data(message: Message) -> None:
    bot.set_state(message.from_user.id, RequestState.city, message.chat.id)
    bot.send_message(message.from_user.id, f'Введи город назначения на английском')


@bot.message_handler(state=RequestState.city)
def get_city(message: Message):
    bot.send_message(message.from_user.id, 'Спасибо, записал! Теперь введи дату заезда в формате YYYY-MM-DD')
    bot.set_state(message.from_user.id, RequestState.check_in_date, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text
    return


@bot.message_handler(state=RequestState.check_in_date)
def get_check_in_date(message):
    if re.match(r'\b\d{4}-\d{2}-\d{2}', message.text):
        bot.send_message(message.from_user.id, 'Спасибо, записал! Теперь введи дату выезда в формате YYYY-MM-DD')
        bot.set_state(message.from_user.id, RequestState.check_out_date, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if checking_date(message.text):
                data['checkin'] = message.text
            else:
                data['checkin'] = current_date

    else:
        bot.send_message(message.from_user.id, 'Неправильный формат даты. Дата должна быть в формате YYYY-MM-DD.\n'
                                               'Например: 1963-11-22')


@bot.message_handler(state=RequestState.check_out_date)
def get_check_out_day(message):
    if re.match(r'\b\d{4}-\d{2}-\d{2}', message.text):
        bot.send_message(message.from_user.id, 'Спасибо, записал! Теперь введите количество взрослых, которые поедут')
        bot.set_state(message.from_user.id, RequestState.adults, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if checking_date(message.text, compare_date=data['checkin']):
                data['checkout'] = message.text
            else:
                data['checkout'] = next_date

    else:
        bot.send_message(message.from_user.id, 'Неправильный формат даты. Дата должна быть в формате YYYY-MM-DD.\n'
                                               'Например: 1963-11-22')


@bot.message_handler(state=RequestState.adults)
def get_adults(message):
    if str(message.text).isdigit():
        bot.send_message(message.from_user.id, 'Спасибо, записал! Теперь введите количество детей, которые поедут')
        bot.set_state(message.from_user.id, RequestState.children, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['adults'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, отправьте количество взрослых числом!\n'
                                               'В вашем сообщении не должно быть букв!')


@bot.message_handler(state=RequestState.children)
def get_children(message):
    if str(message.text).isdigit():
        bot.send_message(message.from_user.id, 'Спасибо, записал! Теперь введите количество младенцев, которые поедут')
        bot.set_state(message.from_user.id, RequestState.infants, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['children'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, отправьте количество детей числом!\n'
                                               'В вашем сообщении не должно быть букв!')


@bot.message_handler(state=RequestState.infants)
def get_infants(message):
    if str(message.text).isdigit():
        bot.send_message(message.from_user.id, 'Спасибо, записал! Теперь введите номер страницы для поиска')
        bot.set_state(message.from_user.id, RequestState.page, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['infants'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, отправьте количество младенцев числом!\n'
                                               'В вашем сообщении не должно быть букв!')


@bot.message_handler(state=RequestState.page)
def get_page(message):
    if str(message.text).isdigit():
        bot.send_message(message.from_user.id, 'Спасибо, записал!')

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['page'] = message.text

        text = f'Спасибо за предоставленную информацию! Данные вашего запроса:\n' \
               f'Город: {data["city"]}\n' \
               f'Дата въезда: {data["checkin"]}\n' \
               f'Дата выезда: {data["checkout"]}\n' \
               f'Количество взрослых: {data["adults"]}\n' \
               f'Количество детей: {data["children"]}\n' \
               f'Количество младенцев: {data["infants"]}\n' \
               f'Страница поиска: {data["page"]}\n'
        bot.send_message(message.from_user.id, text)
        low_offer = get_low(message=message)
        with open(current_request, 'r') as file:
            current_data = json.load(file)
            result = current_data[low_offer]
            save_request(result)
            text = 'Вот ваш вариант!\n'\
                    '\nНазвание: {name}\n'\
                    'Ссылка: {link}\n'\
                    'Рейтинг: {rating}\n'.format(
                    name=result['name'], link=result['url'], rating=result['rating']
        )
            bot.send_message(message.from_user.id, text)
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, отправьте числом номер страницы для поиска!\n'
                                               'В вашем сообщении не должно быть букв!')


def get_low(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        current_response = new_data(
            location=data['city'], checkin=data['checkin'], checkout=data['checkout'],
            adults=data['adults'], children=data['children'], infants=data['infants'],
            page=data['page']
        )
        processing_data(request_dict=current_response)
        current_response = sorting_data()
        return current_response[0]





