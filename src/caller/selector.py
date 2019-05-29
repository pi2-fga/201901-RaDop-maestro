def _action_vehicle_flagrant(dict_msg):
    print('TAKING THE ACTIONS FOR vehicle-flagrant')

def _action_status_radar(dict_msg):
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
    
    dict_actions[type_msg](dict_msg)