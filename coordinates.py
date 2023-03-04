from typing import NamedTuple
from traceback import format_exc
from urllib.request import urlopen
from json.decoder import JSONDecodeError
import json
import ssl

import config
from exceptions import CantGetCoordinates


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


def _get_nominatim_response(query: str, limit: int) -> str:
    ssl._create_default_https_context = ssl._create_unverified_context
    url = config.NOMINATIM_SEARCH_URI.format(query=query, limit=limit)

    try:
        return urlopen(url).read()
    except Exception:
        print(format_exc())
        raise CantGetCoordinates


def _parse_nominatim_response(nominatim_response: str) -> Coordinates:
    try:
        nominatim_dict = json.loads(nominatim_response)
    except JSONDecodeError:
        print(format_exc())
        raise CantGetCoordinates

    return Coordinates(
        latitude=float(nominatim_dict[0]['lat']), 
        longitude=float(nominatim_dict[0]['lon'])
    )


def _get_nominatim_coordinates(place: str) -> Coordinates:
    nominatim_response = _get_nominatim_response(place, 1)
    coordinates = _parse_nominatim_response(nominatim_response)
    return coordinates


def _round_coordinates(coordinates: Coordinates) -> Coordinates:
    if not config.USE_ROUNDED_COORDS:
        return coordinates
    
    return Coordinates(*map(
        lambda c: round(c, 1),
        (coordinates.latitude, coordinates.longitude)
    ))


def get_coordinates(place: str) -> Coordinates:
    """Returns current coordinates using Nominatim API service"""
    coordinates = _get_nominatim_coordinates(place)
    return _round_coordinates(coordinates)
