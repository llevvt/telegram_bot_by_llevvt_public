from loader import bot
from states.request_state import RequestState
from telebot.types import Message
import re
from utils.other_utils.cheking_date import checking_date
from config_data.request_config import current_date, next_date
from keyboards.reply.yes_no import yes_no
from . import history
from utils.data_processing.prepare_for_saving import prepare_for_saving
from typing import Dict, List
import time
from handlers.default_heandlers import help, start


@bot.message_handler(commands=['low', 'high', 'custom'])
def get_data(message: Message) -> None:
    """
    The start function of 'low', 'high' and 'custom' user scripts. It initiates the user script
    and sending the instructions to the user. Also, it redirects user to
    the next stage of the user script - the function get_city.


    :param message: This is a message from the user
    :type message: Message
    """

    bot.set_state(message.from_user.id, RequestState.city, message.chat.id)
    bot.send_message(message.from_user.id, 'Введи город назначения на английском')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = str(message.text)


@bot.message_handler(state=RequestState.city)
def get_city(message: Message) -> None:
    """
    The second function in the user script. It retrieves the data from
    the user about destination city and sends new instructions for the user.
    Also, it redirects user to the next stage of the user script -
    the function get_check_in_date.

    :param message: This is a message from the user
    :type message: Message
    """

    if re.match(r'\b[A-Z][a-z]+\b', message.text):
        bot.send_message(message.from_user.id, 'Спасибо, записал! Теперь введи дату заезда в формате YYYY-MM-DD')
        bot.set_state(message.from_user.id, RequestState.check_in_date, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Неверно введено название города. '
                                               '\nНавание города дольжно быть написано '
                                               'с большой буквы и на английском языке ')


@bot.message_handler(state=RequestState.check_in_date)
def get_check_in_date(message:  Message) -> None:
    """
    The third function in the user script. It retrieves the data
    from the user about check-in date and sends new instructions
    to the user. Also, it redirects user to the next stage of
    the user script - the function get_check_out_date.

    :param message: This is a message from the user
    :type message: Message
    """

    if re.match(r'\b\d{4}-\d{2}-\d{2}\b', message.text):
        bot.send_message(message.from_user.id, 'Спасибо, записал! Теперь введи дату выезда в формате YYYY-MM-DD')
        bot.set_state(message.from_user.id, RequestState.check_out_date, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if checking_date(message.text):
                data['checkin'] = message.text
            else:
                data['checkin'] = str(current_date)

    else:
        bot.send_message(message.from_user.id, 'Неправильный формат даты. Дата должна быть в формате YYYY-MM-DD.\n'
                                               'Например: 1963-11-22')


@bot.message_handler(state=RequestState.check_out_date)
def get_check_out_date(message: Message) -> None:
    """
    The fourth function in the user script. It retrieves the data
    from the user about check-out date and sends new instructions to the user.
    Also, it redirects user to the next stage of the user script -
    the function get_adults.

    :param message: This is a message from the user
    :type message: Message
    """

    if re.match(r'\b\d{4}-\d{2}-\d{2}\b', message.text):
        bot.send_message(message.from_user.id, 'Спасибо, записал! Теперь введите количество взрослых, которые поедут')
        bot.set_state(message.from_user.id, RequestState.adults, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if checking_date(message.text, compare_date=data['checkin']):
                data['checkout'] = message.text
            else:
                data['checkout'] = str(next_date)

    else:
        bot.send_message(message.from_user.id, 'Неправильный формат даты. Дата должна быть в формате YYYY-MM-DD.\n'
                                               'Например: 1963-11-22')


@bot.message_handler(state=RequestState.adults)
def get_adults(message: Message) -> None:
    """
    The fifth function in the user script. It retrieves the data
    from the user about number of an adults date and sends new
    instructions to the user. Also, it redirects user to the next
    stage of the user script - the function if_children.

    :param message: This is a message from the user
    :type message: Message
    """

    if str(message.text).isdigit():
        bot.send_message(message.from_user.id, 'Спасибо, записал! Поедут ли с Вами дети? Для ответа нажмите на кнопку.',
                         reply_markup=yes_no())
        bot.set_state(message.from_user.id, RequestState.children_bool, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['adults'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, отправьте количество взрослых числом!\n'
                                               'В вашем сообщении не должно быть букв!')


@bot.message_handler(state=RequestState.children_bool)
def if_children(message: Message) -> None:
    """
    The sixth function in th user script. This function
    asking user, would the children go. If not, this function
    redirects user to the get_page, otherwise it redirects user to the
    get_children and sends new instructions.

    :param message: This is a message from the user
    :type message: Message
    """

    if message.text == 'Да':
        bot.send_message(message.from_user.id, 'Введите пожалуйста количество детей, которые с Вами поедут')
        bot.set_state(message.from_user.id, RequestState.children, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['children_bool'] = 'Да'
    elif message.text == 'Нет':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['children'] = '0'
            data['infants'] = '0'
            data['children_bool'] = 'Нет'
        bot.send_message(message.from_user.id, 'Спасибо! Теперь введите номер страницы для поиска')
        bot.set_state(message.from_user.id, RequestState.page, message.chat.id)
    else:
        bot.send_message(message.from_user.id, 'Для ответа, пожалуйста, нажмите на кнопку.')


@bot.message_handler(state=RequestState.children)
def get_children(message: Message) -> None:
    """
    This is not essential function in the user script.
    This function retrieves from the message the data about
    children number and redirects the user to the
    next stage of this user script's branch - get_infants.

    :param message: This is a message from the user
    :type message: Message
    """

    if str(message.text).isdigit():
        bot.send_message(message.from_user.id, 'Спасибо, записал! Теперь введите количество младенцев, которые поедут')
        bot.set_state(message.from_user.id, RequestState.infants, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['children'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, отправьте количество детей числом!\n'
                                               'В вашем сообщении не должно быть букв!')


@bot.message_handler(state=RequestState.infants)
def get_infants(message: Message) -> None:
    """
    This is not essential function in the user script.
    This function retrieves from the message the data about
    infants number and redirects the user to the
    next stage of the user script - get_page.

    :param message: This is a message from the user
    :type message: Message
    """

    if str(message.text).isdigit():
        bot.send_message(message.from_user.id, 'Спасибо, записал! Теперь введите номер страницы для поиска')
        bot.set_state(message.from_user.id, RequestState.page, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['infants'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, отправьте количество младенцев числом!\n'
                                               'В вашем сообщении не должно быть букв!')


@bot.message_handler(state=RequestState.page)
def get_page(message: Message) -> None:
    """
    This function retrieve the page number, sends user all received information, sends results
    of the search and ends user script for 'low' and 'high' user scripts, or
    retrieve the page number and redirects user to the get_min_price for
    'custom' user script.

    :param message: This is a message from the user
    :type message: Message
    """

    if str(message.text).isdigit():
        bot.send_message(message.from_user.id, 'Спасибо, записал!')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['page'] = message.text
        if data['command'] == r'/low' or data['command'] == r'/high':

            text = f'Спасибо за предоставленную информацию! Данные вашего запроса:\n' \
                   f'Город: {data["city"]}\n' \
                   f'Дата въезда: {data["checkin"]}\n' \
                   f'Дата выезда: {data["checkout"]}\n' \
                   f'Количество взрослых: {data["adults"]}\n' \
                   f'Количество детей: {data["children"]}\n' \
                   f'Количество младенцев: {data["infants"]}\n' \
                   f'Страница поиска: {data["page"]}\n'
            bot.send_message(message.from_user.id, text)
            result: Dict = prepare_for_saving(message=message, command=data['command'])
            text = 'Вот ваш вариант!\n'\
                'Название: {name}\n'\
                'Ссылка: {link}\n'\
                'Рейтинг: {rating}\n' \
                'Стоимость: {price}$'.format(
                    name=result['name'], link=result['url'], rating=result['rating'], price=result['price']
                    )

            bot.send_message(message.from_user.id, text)
            bot.set_state(message.from_user.id, None, message.chat.id)
        elif data['command'] == r'/custom':
            bot.send_message(message.from_user.id, 'Теперь введите минимальную стоимость для поиска')
            bot.set_state(message.from_user.id, RequestState.min_price, message.chat.id)
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, отправьте числом номер страницы для поиска!\n'
                                               'В вашем сообщении не должно быть букв!')


@bot.message_handler(state=RequestState.min_price)
def get_min_price(message: Message) -> None:
    """
    This function retrieves form the user minimal price for the
    custom search and then redirects the user to the get_max_price.

    :param message: This is a message from the user
    :type message: Message
    """

    if str(message.text).isdigit():
        bot.send_message(message.from_user.id, 'Спасибо, записал! Теперь введите максимальную стоимость для поиска')
        bot.set_state(message.from_user.id, RequestState.max_price, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['min_price'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, отправьте минимальную стоимость числом!\n'
                                               'В вашем сообщении не должно быть букв!')


@bot.message_handler(state=RequestState.max_price)
def get_max_price(message: Message) -> None:
    """
    This function retrieves maximal price for the custom search.
    Then this function executes custom search with the provided
    parameters and sends results of the search to the user.
    Also, this function ends 'custom' user script.

    :param message: This is a message from the user
    :type message: Message
    """

    if str(message.text).isdigit():
        bot.send_message(message.from_user.id, 'Спасибо, записал!')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['max_price'] = message.text
        text = f'Спасибо за предоставленную информацию! Данные вашего запроса:\n' \
               f'Город: {data["city"]}\n' \
               f'Дата въезда: {data["checkin"]}\n' \
               f'Дата выезда: {data["checkout"]}\n' \
               f'Количество взрослых: {data["adults"]}\n' \
               f'Количество детей: {data["children"]}\n' \
               f'Количество младенцев: {data["infants"]}\n' \
               f'Страница поиска: {data["page"]}\n' \
               f'Диапозон цен для поиска: {data["min_price"]}- {data["max_price"]}$'
        bot.send_message(message.from_user.id, text)
        result: List[Dict] = prepare_for_saving(
                                                message=message, command=data['command'],
                                                parameters=[int(data['min_price']), int(data['max_price'])]
                                                )
        if len(result) != 0:
            for i_result in result:
                text = 'Вот ваш вариант!\n' \
                       '\nНазвание: {name}\n' \
                       'Ссылка: {link}\n' \
                       'Рейтинг: {rating}\n' \
                       'Стоимость: {price}$'.format(
                        name=i_result['name'], link=i_result['url'], rating=i_result['rating'], price=i_result['price']
                        )
                bot.send_message(message.from_user.id, text)
                time.sleep(0.5)
            bot.set_state(message.from_user.id, None, message.chat.id)
        else:
            bot.send_message(message.from_user.id, 'Мы ничего не нашли ничего за такую цену, '
                                                   'попробуйте изменить диапозон\n'
                                                   'Пожалуйста, ведите минимальную цену для поиска')
            bot.set_state(message.from_user.id, RequestState.min_price, message.chat.id)
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, отправьте максимальную стоимость числом!\n'
                                               'В вашем сообщении не должно быть букв!')
