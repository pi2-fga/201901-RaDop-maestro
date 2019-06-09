from . import communication, triage


def _action_vehicle_flagrant(dict_payload):
    print('TAKING THE ACTIONS FOR vehicle-flagrant')
    # send the image to get plate's candidates
    if triage.valid_base64(dict_payload['image1']):
        dict_plates_identification = communication.search_plate(dict_payload['image1'])
    elif triage.valid_base64(dict_payload['image2']):
        dict_plates_identification = communication.search_plate(dict_payload['image2'])
    else:
        print('INFO No valid images found! ending the function.')
        return None
    print(f'result of search_plate: {dict_plates_identification}')

    # extract the best plate from the candidates
    plate = triage.extract_plate(dict_plates_identification)
    print(f'result of extract_plate: {plate}')

    # check for informations from the vehicle
    vehicle_data = communication.get_vehicle_info(plate)
    print(f'result of get_vehicle_info: {vehicle_data}')

    # save the data in db
    print('SAVING DATA IN RETHINK')

    pass


def _action_status_radar(dict_payload):
    print('TAKING THE ACTIONS FOR status-radar')

dict_actions = {
    'vehicle-flagrant': _action_vehicle_flagrant,
    'status-radar': _action_status_radar
}


def select_action(dict_msg):
    try:
        type_msg = dict_msg['type']
    except:
        print('\t[*] Error trying to identify the type of the message! No actions will be taken!')

    dict_actions[type_msg](dict_msg['payload'])