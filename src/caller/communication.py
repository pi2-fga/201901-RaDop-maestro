# module with functions to communicate with the microsservices
import json
import requests
import os
import uuid
import datetime

LOCALHOST = '0.0.0.0'

MSERVICES_HOST = os.getenv('MSERVICES_HOST', 'localhost')
ALPR_PORT = os.getenv('ALPR_PORT', 8080)
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

def search_plate(dict_vehicle = None):
    uuid = _generate_id()
    time = _get_time()

    if dict_vehicle:
        dict_json = {
            "id": uuid,
            "type": "alpr-call",
            "payload": {
                "key": ALPR_KEY,
                "image": dict_vehicle['payload']['image']
            },
            "time": time
        }

        response = _do_request(dict_json, 'POST', f'{MSERVICES_HOST}:{ALPR_PORT}/function/fn-alpr')

        if response.status_code == 200:
            response.json()

            return response['response']['results']
        else:
            return None

    else:
        return None

