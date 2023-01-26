from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def yes_no() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(KeyboardButton('Да'))
    keyboard.add(KeyboardButton('Нет'))
    return keyboard
