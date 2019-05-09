import json
import time

# take the json payload from the message body and transform in a dictionary
def parse_json_dict(message_body):
    parse = None
    try:
        parse = json.loads(message_body)
    except:
        print('\t[*] Houve erro na decodificação do payload!')
    return parse

def triage(message_body):
    # json -> dictionary
    dict_payload = parse_json_dict(message_body)

    print(f'dicionário gerado: {dict_payload}')
