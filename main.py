from loader import bot
from utils.set_bot_commands import set_default_commands
import handlers


if __name__ == '__main__':
    set_default_commands(bot)
    bot.infinity_polling()
