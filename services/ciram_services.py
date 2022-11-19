import requests
from settings import CIRAM_URL

def post_ciram(data: dict):
    json_data = str(data)  # ciram expects single quotes
    try:
        _ = requests.post(CIRAM_URL, json=json_data, headers={"Content-Type": "application/json"})
        print(f'Message was sent to ciram')
    except requests.exceptions.ConnectionError:
        print('Cannot connect to ciram')
