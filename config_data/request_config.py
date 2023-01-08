import os
from datetime import datetime, timedelta

HEADERS = {
    'X-RapidApi-Key': os.getenv('X-RAPIDAPI-KEY'),
    'X-RapidApi-Host': os.getenv('X-RAPIDAPI-HOST')
}

querystring = {
    "location": "Paris", "checkin": "2022-05-16", "checkout": "2022-05-17",
    "adults": "1", "children": "0", "infants": "0", "page": "1"
}

url = "https://airbnb13.p.rapidapi.com/search-location"

current_date = datetime.now().date()
next_date = datetime.now().date() + timedelta(days=1)


needed_parameters_of_hotel = (
    'url', 'name', 'bathrooms', 'bedrooms', 'beds', 'city',
    'persons', 'rating', 'type', 'price'
)
