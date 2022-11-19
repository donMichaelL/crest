import requests

from typing import Union
from settings import NATIONAL_DB_VEHICLE

COLOR_STOLEN = Union[str, bool]

def get_vehicle_attributes(plate) -> COLOR_STOLEN:
    response = requests.get(NATIONAL_DB_VEHICLE + plate)
    try:
        msg = response.json()[0]
        if msg['stolen'] == 'true':
            return msg["color"], True
        return msg["color"], False
    except Exception as err:
        return None, False