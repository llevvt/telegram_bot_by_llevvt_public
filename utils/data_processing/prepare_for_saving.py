from telebot.types import Message
from utils.data_processing.save_request import save_request
from loader import bot
from utils.data_processing.get_data import new_data
from utils.data_processing.processing_data import processing_data
from utils.data_processing.sorting_data import sorting_data
from typing import List


def prepare_for_saving(message, command, parameters: List[int] = None):
    offer, current_data = get_offer(message=message, command=command, parameters=parameters)
    parameters_for_message = ('name', 'url', 'rating', 'price')
    if command == 'low' or command == 'high':
        result = current_data[offer]
        for i_param in parameters_for_message:
            if i_param not in result.keys():
                result[i_param] = 'Нет информации'
        save_request(result, user_id=message.from_user.id)
    elif command == 'custom':
        result = list()
        for i_id in offer:
            for i_param in parameters_for_message:
                if i_param not in current_data[id].keys():
                    current_data[i_id][i_param] = 'Нет информации'
            result.append(current_data[i_id])
            save_request(current_data[i_id], user_id=message.from_user.id)
    return result


def get_offer(message: Message, command: str, parameters: List[int] = None) -> List or str:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        current_response = new_data(
            location=data['city'], checkin=data['checkin'], checkout=data['checkout'],
            adults=data['adults'], children=data['children'], infants=data['infants'],
            page=data['page']
        )
    sorted_dict = processing_data(request_dict=current_response)
    current_response = sorting_data(sorted_dict)
    if command == r'/low':
        return current_response[0], sorted_dict
    elif command == r'/high':
        return current_response[len(current_response) - 1], sorted_dict
    elif command == r'/custom':
        new_list = list()
        for i_id in current_response:
            if parameters[0] <= sorted_dict[current_response]['price'] <= parameters[1]:
                new_list.append(i_id)
        return new_list, sorted_dict
