import requests

from settings import FUSION_GEO

def check_server_for_restricted_area(camera_name: str):
    payload= [('deviceID', camera_name)]
    try:
        r = requests.get(FUSION_GEO + 'check-camera/' , params=payload)
        data = r.json()
        if data['found_areas'] == True:
            return ('High', 'Vehicle in restricted area', data['area'])
        else:
            return ('Medium', 'Vehicle NOT in restricted area', None)
    except Exception as err:
        return ('Medium', 'Vehicle NOT in restricted area', None)


def publish_to_geo_areas(msg):
    headers = {"Content-Type": "application/json"}
    try:
        _ = requests.post(FUSION_GEO + 'set-areas/' , data=msg, headers=headers)
        print(f'Message was sent to geo with cameras and areas')
    except requests.ConnectionError as err:
        print(err)