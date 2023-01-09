from config_data.pathes_data import history_path
import json


def save_request(request_dict):
    with open(history_path, 'a') as file:
        history = json.load(file)
#         if len(history.keys()) < 10:

