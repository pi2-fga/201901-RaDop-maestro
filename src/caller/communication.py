import json
import requests
import os
import uuid
import datetime

ALPR_KEY = os.getenv('ALPR_KEY', '')
ALPR_HOST = os.getenv('ALPR_HOST', 'localhost')
ALPR_PORT = os.getenv('ALPR_PORT', 8080)
SINESP_DOMAIN = os.getenv('SINESP_DOMAIN', '')


def _generate_id():
    identifier = str(uuid.uuid4())
    return identifier


def _get_time():
    time = datetime.datetime.utcnow()
    time = str(time.isoformat('T') + 'Z')
    return time


def search_plate(image_vehicle = None):
    if image_vehicle:
        uuid = _generate_id()
        time = _get_time()
        dict_json = {
            "id": uuid,
            "type": "alpr-call",
            "payload": {
                "key": ALPR_KEY,
                "image": image_vehicle
            },
            "time": time
        }

        response = requests.post(f'http://{ALPR_HOST}:{ALPR_PORT}/function/fn-alpr', json=dict_json)

        dict_response = response.json()
        if dict_response['status_code'] == 200:
            return dict_response
        else:
            return None

    else:
        return None


def get_vehicle_info(plate = None):
    if plate:
        uuid = _generate_id()
        time = _get_time()
        dict_json = {
            "id": uuid,
            "type": "sinesp-call",
            "payload": {
                "plate": plate
            },
            "time": time
        }

        response = requests.post(f'http://{SINESP_DOMAIN}/function/fn-sinesp', json=dict_json)

        dict_response = response.json()
        if dict_response['status_code'] == 200:
            return dict_response
        else:
            return None

    else:
        return None
