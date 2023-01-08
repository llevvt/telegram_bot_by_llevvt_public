from config_data.request_config import needed_parameters_of_hotel
from config_data.pathes_data import current_request
from typing import Dict
import json


def processing_data(request_dict: Dict) -> None:
    new_dict = dict()
    for i_result in request_dict['results']:
        current_id = i_result["id"]
        new_dict[current_id] = dict()
        for i_parameter in i_result.keys():
            if i_parameter in needed_parameters_of_hotel:
                try:
                    if i_parameter == 'price':
                        new_dict[current_id][i_parameter] = i_result[i_parameter]['total']
                    else:
                        new_dict[current_id][i_parameter] = i_result[i_parameter]
                except KeyError:
                    if i_parameter in needed_parameters_of_hotel[2:]:
                        new_dict[current_id][i_parameter] = 0
                    else:
                        new_dict[current_id][i_parameter] = None

    with open(current_request, 'w') as file:
        json.dump(new_dict, file, indent=4)
