import json
import re
import logging

LOG_FORMAT = ('%(asctime)s %(levelname)10s - %(name)s %(funcName)s:\n%(message)s')
LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.INFO)


def transform_json_payload(message_body):
    dict_payload = None
    try:
        dict_payload = json.loads(message_body)
    except Exception as err:
        LOGGER.error(exc_info=True)

    # LOGGER.debug(f'generated dictionary: {dict_payload}')
    return dict_payload


# extract the best candidate to a vehicle's plate
def extract_plate(dict_json):
    if dict_json:
        candidates_alpr = dict_json['response']['results'][0]['candidates']
        plate = None
        best_confidence = -1

        for candidate in candidates_alpr:
            if candidate['matches_template'] == 1 and candidate['confidence'] > best_confidence:
                plate = candidate['plate']
                best_confidence = candidate['confidence']

        LOGGER.debug(f'The best plate id is: {plate}')
        return plate
    else:
        LOGGER.warning('No plate was extracted from the data informed!')
        return None


def valid_base64(str_base64):
    if str_base64:
        pattern = re.compile("^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)$")
        return bool(pattern.match(str_base64))

    else:
        return False
