import json
import re

# take the json payload from the message body and transform in a dictionary
def transform_json_payload(message_body):
    # json -> dictionary
    dict_payload = None
    try:
        dict_payload = json.loads(message_body)
    except:
        print('\t[*] Error in payload\'s decodification!')
    
    print(f'generated dictionary: {dict_payload}')
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

        print(f'The best plate id is: {plate}')
        return plate
    else:
        return None


def valid_base64(str_base64):
    if str_base64:
        pattern = re.compile("^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)$")
        return bool(pattern.match(str_base64))

    else:
        return False
