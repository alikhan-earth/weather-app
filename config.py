import os

from dotenv import load_dotenv

load_dotenv()

USE_ROUNDED_COORDS = False
NOMINATIM_SEARCH_URI = (
    'https://nominatim.openstreetmap.org/search'
    '?q={query}'
    '&format=json'
    '&limit={limit}'
)
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
OPENWEATHER_URI = (
    'https://api.openweathermap.org/data/2.5/weather'
    '?lat={latitude}&lon={longitude}'
    '&appid=' + OPENWEATHER_API_KEY + '&lang=ru'
    '&units=metric'
)
