import re
import csv
from typing import List
from pathlib import Path
from loguru import logger
# from qrz import get_locator_from_qrz

def read_csv_to_list_of_tuples(filename: str):
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        return [tuple(row) for row in csv_reader]
grandparent_folder = Path(__file__).parents[1]
callsign_to_locator_filename = f"{grandparent_folder}/src/prefixes_list.csv"
# if debug:
#     logger.debug(f"{callsign_to_locator_filename=}")
PREFIXES_TO_LOCATORS = read_csv_to_list_of_tuples(filename=callsign_to_locator_filename)


class Position:
    def __init__(self, lat:float, lon:float):
        self.lat = lat
        self.lon = lon
    def __str__(self):
        return f"{self.lat},{self.lon}"





def resolve_locator(
        callsign:str, 
        # prefixes_to_locators:List
    ) -> str:
    callsign=callsign.upper()
    for regex, locator, country, continent in PREFIXES_TO_LOCATORS:
        if re.match(regex+".*", callsign):
            return locator
    return None

# def resolve_country(callsign:str, prefixes_to_locators:List) -> str:
#     callsign=callsign.upper()
#     for regex, _, country in prefixes_to_locators:
#         if re.match(regex+".*", callsign):
#             return country
#     return None


def resolve_country_and_continent(
        callsign:str, 
        # prefixes_to_locators:List
    ):
    callsign=callsign.upper()
    for regex, locator, country, continent in PREFIXES_TO_LOCATORS:
        if re.match(regex+".*", callsign):
            return country, continent
    return None, None


def locator_to_coordinates(locator: str) -> dict:
    if locator:
        # Many thanks to Dmitry (4X5DM) for the algorithm

        # Constants
        ASCII_0 = 48
        ASCII_A = 65
        ASCII_a = 97
        # Validate input
        assert isinstance(locator, str)
        assert 4 <= len(locator) <= 8
        assert len(locator) % 2 == 0

        locator = locator.upper()

        # Separate fields, squares and subsquares
        # Fields
        lon_field = ord(locator[0]) - ASCII_A
        lat_field = ord(locator[1]) - ASCII_A

        # Squares
        lon_sq = ord(locator[2]) - ASCII_0
        lat_sq = ord(locator[3]) - ASCII_0

        # Subsquares
        if len(locator) >= 6:
            lon_sub_sq = ord(locator[4]) - ASCII_A
            lat_sub_sq = ord(locator[5]) - ASCII_A
        else:
            lon_sub_sq = 0
            lat_sub_sq = 0

        # Extended squares
        if len(locator) == 8:
            lon_ext_sq = ord(locator[6]) - ASCII_0
            lat_ext_sq = ord(locator[7]) - ASCII_0
        else:
            lon_ext_sq = 0
            lat_ext_sq = 0

        # Calculate latitude and longitude
        lon = -180.0
        lat = -90.0

        lon += 20.0 * lon_field
        lat += 10.0 * lat_field

        lon += 2.0 * lon_sq
        lat += 1.0 * lat_sq

        lon += 5.0 / 60 * lon_sub_sq
        lat += 2.5 / 60 * lat_sub_sq

        lon += 0.5 / 60 * lon_ext_sq
        lat += 0.25 / 60 * lat_ext_sq

        return float(int(lat*10000))/10000, float(int(lon*10000))/10000
    
    else:
        return None, None


