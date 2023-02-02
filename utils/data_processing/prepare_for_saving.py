from telebot.types import Message
from config_data.pathes_data import current_request
from utils.data_processing.save_request import save_request
from loader import bot
import json
from utils.data_processing.get_data import new_data
from utils.data_processing.processing_data import processing_data
from utils.data_processing.sorting_data import sorting_data


def prepare_for_saving(message, command):
    low_offer = get_low(message=message, command=command)
    with open(current_request, 'r') as file:
        current_data = json.load(file)
    result = current_data[low_offer]
    parameters_for_message = ('name', 'url', 'rating', 'price')
    for i_param in parameters_for_message:
        if i_param not in result.keys():
            result[i_param] = 'Нет информации'
    save_request(result, user_id=message.from_user.id)
    return result


def get_low(message: Message, command):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        current_response = new_data(
            location=data['city'], checkin=data['checkin'], checkout=data['checkout'],
            adults=data['adults'], children=data['children'], infants=data['infants'],
            page=data['page']
        )
        processing_data(request_dict=current_response)
        current_response = sorting_data()
        if command == 'low':
            return current_response[0]
        elif command == 'high':
            return current_response[len(current_response) - 1]