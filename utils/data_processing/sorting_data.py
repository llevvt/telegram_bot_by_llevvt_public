from typing import List
import json
from config_data.pathes_data import current_request


def sorting_data(parameter: str = 'price') -> List:
    with open(current_request, 'r') as file:
        current_data = json.load(file)
        start_massive = list(current_data.keys())
        result = quick_sorting(start_massive, current_data, parameter)
        return result


def quick_sorting(massive, data, parameter) -> List:
    if len(massive) < 2:
        return massive
    else:
        reference_id = massive[0]
        less = [i_id for i_id in massive[1:] if data[i_id][parameter] < data[reference_id][parameter]]
        more = [i_id for i_id in massive[1:] if data[i_id][parameter] >= data[reference_id][parameter]]
        return quick_sorting(massive=less, data=data, parameter=parameter) + \
               [reference_id] + quick_sorting(massive=more, data=data, parameter=parameter)