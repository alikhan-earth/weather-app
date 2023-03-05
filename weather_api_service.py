from datetime import datetime
from typing import NamedTuple, Literal
from traceback import format_exc
from enum import Enum
from urllib.request import urlopen
from json.decoder import JSONDecodeError
import json
import ssl

import config
from exceptions import WeatherApiServiceError
from coordinates import Coordinates

Celsius = float


class WeatherType(Enum):
    THUNDERSTORM = 'Гроза'
    DRIZZLE = 'Изморозь'
    RAIN = 'Дождь'
    SNOW = 'Снег'
    CLEAR = 'Ясно'
    FOG = 'Туман'
    CLOUDS = 'Облачно'


class Weather(NamedTuple):
    temperature: Celsius
    feels_like: Celsius
    weather_type: WeatherType
    sunrise: datetime
    sunset: datetime


def _get_openweather_response(latitude: float, longitude: float) -> str:
    ssl._create_default_https_context = ssl._create_unverified_context
    url = config.OPENWEATHER_URI.format(latitude=latitude, longitude=longitude)

    try:
        return urlopen(url).read()
    except Exception:
        print(format_exc())
        raise WeatherApiServiceError


def _parse_temperature(openweather_dict: dict) -> Celsius:
    try:
        return openweather_dict['main']['temp']
    except KeyError:
        print(format_exc())
        raise WeatherApiServiceError
    

def _parse_feels_like_temperature(openweather_dict: dict) -> Celsius:
    try:
        return openweather_dict['main']['feels_like']
    except KeyError:
        print(format_exc())
        raise WeatherApiServiceError


def _parse_weather_type(openweather_dict: dict) -> WeatherType:
    try:
        weather_type_id = str(openweather_dict['weather'][0]['id'])
    except (KeyError, IndexError):
        print(format_exc())
        raise WeatherApiServiceError

    weather_types = {
        '1': WeatherType.THUNDERSTORM,
        '3': WeatherType.DRIZZLE,
        '5': WeatherType.RAIN,
        '6': WeatherType.SNOW,
        '7': WeatherType.FOG,
        '800': WeatherType.CLEAR,
        '80': WeatherType.CLOUDS,
    }

    for _id, _weather_type in weather_types.items():
        if weather_type_id.startswith(_id):
            return _weather_type
    print(weather_type_id)
    raise WeatherApiServiceError
    

def _parse_sun_time(
        openweather_dict: dict, 
        time_type: Literal['sunrise'] | Literal['sunset']) -> datetime:
    return datetime.fromtimestamp(openweather_dict['sys'][time_type])


def _parse_openweather_response(openweather_response: str) -> Weather:
    try:
        openweather_dict = json.loads(openweather_response)
    except JSONDecodeError:
        print(format_exc())
        raise WeatherApiServiceError

    return Weather(
        temperature=_parse_temperature(openweather_dict),
        feels_like=_parse_feels_like_temperature(openweather_dict),
        weather_type=_parse_weather_type(openweather_dict),
        sunrise=_parse_sun_time(openweather_dict, 'sunrise'),
        sunset=_parse_sun_time(openweather_dict, 'sunset'),
    )


def get_weather(coordinates: Coordinates) -> Weather:
    """Requests weather on OpenWeather API and returns it"""
    openweather_response = _get_openweather_response(
        coordinates.latitude, coordinates.longitude
    )
    weather = _parse_openweather_response(openweather_response)
    return weather
