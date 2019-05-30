import json
import time

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

