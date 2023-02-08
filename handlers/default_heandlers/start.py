from telebot.types import Message
from loader import bot
from handlers.custom_handlers import commands_handler, history, survey


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    bot.reply_to(message, 'Привет, {user_name}!\n'
                          'Я- бот, который может подходящее тебе жилье на airbnb.com\n'
                          r'Чтобы узнать, что я могу, выбери команду \help'.format(user_name = message.from_user.full_name))