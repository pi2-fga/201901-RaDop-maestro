import json
import requests
import os
import uuid
import datetime

LOCALHOST = '0.0.0.0'

MSERVICES_HOST = os.getenv('MSERVICES_HOST', 'localhost')
ALPR_PORT = os.getenv('ALPR_PORT', 8080)
SINESP_PORT = os.getenv('ALPR_PORT', 8080)
ALPR_KEY = os.getenv('ALPR_KEY', '')


def _do_request(dict_json, verb, url):
    request_json = json.dumps(dict_json)

    response = requests.request(verb, url, json=request_json)
    return response


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

        response = _do_request(dict_json, 'POST', f'http://{MSERVICES_HOST}:{ALPR_PORT}/function/fn-alpr')

        dict_response = response.json()

        if dict_response['status_code'] == 200:
            return response
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

        response = _do_request(dict_json, 'POST', f'http://{MSERVICES_HOST}:{SINESP_PORT}/function/fn-sinesp')

        dict_response = response.json()

        if dict_response['status_code'] == 200:
            return response
        else:
            return None

    else:
        return None
