from loader import bot
from states.low_state import LowState
from telebot.types import Message
import re
from utils.other_utils.cheking_date import checking_date
from config_data.request_config import current_date, next_date
from keyboards.reply.yes_no import yes_no
from . import high, history, survey
from utils.data_processing.prepare_for_saving import prepare_for_saving


@bot.message_handler(commands=['low'])
def get_data(message: Message) -> None:
    bot.set_state(message.from_user.id, LowState.city, message.chat.id)
    bot.send_message(message.from_user.id, 'Введи город назначения на английском')


@bot.message_handler(state=LowState.city)
def get_city(message: Message):
    if re.match(r'\b[A-Z][a-z]+\b', message.text):
        bot.send_message(message.from_user.id, 'Спасибо, записал! Теперь введи дату заезда в формате YYYY-MM-DD')
        bot.set_state(message.from_user.id, LowState.check_in_date, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Неверно введено название города. '
                                               '\nНавание города дольжно быть написано '
                                               'с большой буквы и на английском языке ')


@bot.message_handler(state=LowState.check_in_date)
def get_check_in_date(message):
    if re.match(r'\b\d{4}-\d{2}-\d{2}\b', message.text):
        bot.send_message(message.from_user.id, 'Спасибо, записал! Теперь введи дату выезда в формате YYYY-MM-DD')
        bot.set_state(message.from_user.id, LowState.check_out_date, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if checking_date(message.text):
                data['checkin'] = message.text
            else:
                data['checkin'] = str(current_date)

    else:
        bot.send_message(message.from_user.id, 'Неправильный формат даты. Дата должна быть в формате YYYY-MM-DD.\n'
                                               'Например: 1963-11-22')


@bot.message_handler(state=LowState.check_out_date)
def get_check_out_day(message):
    if re.match(r'\b\d{4}-\d{2}-\d{2}\b', message.text):
        bot.send_message(message.from_user.id, 'Спасибо, записал! Теперь введите количество взрослых, которые поедут')
        bot.set_state(message.from_user.id, LowState.adults, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if checking_date(message.text, compare_date=data['checkin']):
                data['checkout'] = message.text
            else:
                data['checkout'] = str(next_date)

    else:
        bot.send_message(message.from_user.id, 'Неправильный формат даты. Дата должна быть в формате YYYY-MM-DD.\n'
                                               'Например: 1963-11-22')


@bot.message_handler(state=LowState.adults)
def get_adults(message):
    if str(message.text).isdigit():
        bot.send_message(message.from_user.id, 'Спасибо, записал! Поедут ли с Вами дети? Для ответа нажмите на кнопку.',
                         reply_markup=yes_no())
        bot.set_state(message.from_user.id, LowState.children_bool, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['adults'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, отправьте количество взрослых числом!\n'
                                               'В вашем сообщении не должно быть букв!')


@bot.message_handler(state=LowState.children_bool)
def if_children(message):
    if message.text == 'Да':
        bot.send_message(message.from_user.id, 'Введите пожалуйста количество детей, которые с Вами поедут')
        bot.set_state(message.from_user.id, LowState.children, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['children_bool'] = 'Да'
    elif message.text == 'Нет':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['children'] = '0'
            data['infants'] = '0'
            data['children_bool'] = 'Нет'
        bot.send_message(message.from_user.id, 'Спасибо! Теперь введите номер страницы для поиска')
        bot.set_state(message.from_user.id, LowState.page, message.chat.id)
    else:
        bot.send_message(message.from_user.id, 'Для ответа, пожалуйста, нажмите на кнопку.')


@bot.message_handler(state=LowState.children)
def get_children(message):
    if str(message.text).isdigit():
        bot.send_message(message.from_user.id, 'Спасибо, записал! Теперь введите количество младенцев, которые поедут')
        bot.set_state(message.from_user.id, LowState.infants, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['children'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, отправьте количество детей числом!\n'
                                               'В вашем сообщении не должно быть букв!')


@bot.message_handler(state=LowState.infants)
def get_infants(message):
    if str(message.text).isdigit():
        bot.send_message(message.from_user.id, 'Спасибо, записал! Теперь введите номер страницы для поиска')
        bot.set_state(message.from_user.id, LowState.page, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['infants'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, отправьте количество младенцев числом!\n'
                                               'В вашем сообщении не должно быть букв!')


@bot.message_handler(state=LowState.page)
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
        result = prepare_for_saving(message=message, command='low')
        text = 'Вот ваш вариант!\n'\
                '\nНазвание: {name}\n'\
                'Ссылка: {link}\n'\
                'Рейтинг: {rating}\n' \
               'Стоимость: {price}$'.format(
                name=result['name'], link=result['url'], rating=result['rating'], price=result['price']
    )

        bot.send_message(message.from_user.id, text)
        bot.set_state(message.from_user.id, None)
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, отправьте числом номер страницы для поиска!\n'
                                               'В вашем сообщении не должно быть букв!')