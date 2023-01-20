from config_data.pathes_data import history_path
import json
from typing import Dict
import os


def save_request(request_dict):
    if os.path.exists(history_path):
        with open(history_path, 'r') as file:
            current_dict = json.load(file)
    else:
        current_dict = dict()
    with open(history_path, 'w') as file:
        if not (0 < len(current_dict.keys()) < 10):
            for i_key in current_dict.keys():
                if i_key == 0:
                    current_dict[i_key - 1] = current_dict[i_key]
        current_dict[len(current_dict.keys())] = request_dict
        json.dump(current_dict, file, indent=4)
