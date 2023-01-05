from telebot.types import Message
from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    bot.reply_to(message, 'Привет, {user_name}!'.format(user_name = message.from_user.full_name))