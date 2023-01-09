from telebot.handler_backends import State, StatesGroup


class RequestState(StatesGroup):
    city = State()
    check_in_date = State()
    check_out_date = State()