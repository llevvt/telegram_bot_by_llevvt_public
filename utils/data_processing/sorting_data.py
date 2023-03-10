from typing import List, Dict, AnyStr


def sorting_data(current_data: Dict, parameter: str = 'price') -> List:
    # with open(current_request, 'r') as file:
    #     current_data = json.load(file)
    start_massive = list(current_data.keys())
    result = quick_sorting(start_massive, current_data, parameter)
    return result


def quick_sorting(massive: List, data: Dict, parameter: AnyStr) -> List:
    if len(massive) < 2:
        return massive
    else:
        reference_id = massive[0]
        less = [i_id for i_id in massive[1:] if data[i_id][parameter] < data[reference_id][parameter]]
        more = [i_id for i_id in massive[1:] if data[i_id][parameter] >= data[reference_id][parameter]]
        return quick_sorting(massive=less, data=data, parameter=parameter) + \
               [reference_id] + quick_sorting(massive=more, data=data, parameter=parameter)