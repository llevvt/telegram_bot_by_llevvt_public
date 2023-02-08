from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS
from loader import bot
from handlers.custom_handlers import commands_handler, history, survey



@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, '\n'.join(text))
