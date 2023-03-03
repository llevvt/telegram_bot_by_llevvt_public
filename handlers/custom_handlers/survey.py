from keyboards.reply.contact import request_contact
from loader import bot
from states.contact_information import UserInfoState
from telebot.types import Message
from handlers.custom_handlers import history, commands_handler
from handlers.default_heandlers import help, start


@bot.message_handler(commands=['survey'])
def survey(message: Message) -> None:
    """
    The first function in the user script 'survey'. This
    function starts script and sends user the welcome message.
    Also, it redirects user to the get_name.

    :param message: This is a message from the user
    :type message: Message
    """

    bot.set_state(message.from_user.id, UserInfoState.name, message.chat.id)
    bot.send_message(message.from_user.id, f'Привет, {message.from_user.username}, введи свое имя')


@bot.message_handler(state=UserInfoState.name)
def get_name(message: Message) -> None:
    """
    The second function in the user script 'survey'.
    This function retrieves name of the user and redirects
    user to the get_age.

    :param message: This is a message from the user
    :type message: Message
    """

    if message.text.isalpha():
        bot.send_message(message.from_user.id, 'Спасибо, записал! Теперь введи свой возраст')
        bot.set_state(message.from_user.id, UserInfoState.age, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['name'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Имя может содержать только буквы!')


@bot.message_handler(state=UserInfoState.age)
def get_age(message: Message) -> None:
    """
    The third function in the user script 'survey'.
    This function retrieves age of the user and redirects
    user to the get_country.

    :param message: This is a message from the user
    :type message: Message
    """

    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Спасибо, записал! Теперь введи страну проживания')
        bot.set_state(message.from_user.id, UserInfoState.country, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['age'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Возраст может быть только числом!')


@bot.message_handler(state=UserInfoState.country)
def get_country(message: Message) -> None:
    """
    The fourth function in the user script 'survey'.
    This function retrieves country of the user and redirects
    user to the get_city.

    :param message: This is a message from the user
    :type message: Message
    """

    bot.send_message(message.from_user.id, 'Спасибо, записал! Теперь введи город проживания')
    bot.set_state(message.from_user.id, UserInfoState.city, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['country'] = message.text


@bot.message_handler(state=UserInfoState.city)
def get_city(message: Message) -> None:
    """
    The fifth function in the user script 'survey'.
    This function retrieves city of the user and redirects
    user to the get_contact.

    :param message: This is a message from the user
    :type message: Message
    """
    bot.send_message(message.from_user.id, 'Спасибо, записал! Отправь свой номер, нажав на кнопку',
                     reply_markup=request_contact())
    bot.set_state(message.from_user.id, UserInfoState.phone_number, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text


@bot.message_handler(content_types=['text', 'contact'], state=UserInfoState.phone_number)
def get_contact(message: Message):
    """
    The sixth function in the user script 'survey'.
    This function retrieves contact information of the user,
    sends all received information to the user and
    ends 'survey' user script.

    :param message: This is a message from the user
    :type message: Message
    """
    if message.content_type == 'contact':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['phone_number'] = message.contact.phone_number

            text = f'Спасибо за предоставленную информацию! Ваши данные:\n' \
                   f'Имя: {data["name"]}\n' \
                   f'Возраст: {data["age"]}\n' \
                   f'Страна: {data["country"]}\n' \
                   f'Город: {data["city"]}\n' \
                   f'Номер телефона: {data["phone_number"]}'
            bot.send_message(message.from_user.id, text)
    else:
        bot.send_message(message.from_user.id, 'Чтобы отправить контактную информацию, нажми на кнопку!')
