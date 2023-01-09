import requests
from config_data.request_config import HEADERS, querystring, url, current_date, next_date
import json
from typing import Dict


def new_data(location: str = 'Paris', checkin: str = str(current_date), checkout: str = str(next_date),
             adults: str = '1',
             children: str = '0', infants: str = '0', page: str = '0') -> Dict:
    querystring["location"] = location
    querystring["checkin"] = checkin
    querystring["checkout"] = checkout
    querystring["adults"] = adults
    querystring["children"] = children
    querystring["infants"] = infants
    querystring["page"] = page
    new_response = requests.get(url=url, headers=HEADERS, params=querystring)
    new_data = json.loads(new_response.text)
    return new_data
    