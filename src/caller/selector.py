import logging
from . import communication, triage

LOG_FORMAT = ('%(asctime)s %(levelname)10s - %(name)s %(funcName)s:\n%(message)s')
LOGGER = logging.getLogger(__name__)


def _action_vehicle_flagrant(infraction_data):
    LOGGER.info('Starting the actions for vehicle flagrant')
    communication.rdm_insert_audit(infraction_data)

    if triage.valid_base64(infraction_data['image1']):
        dict_plates_identification = communication.search_plate(
                                                    infraction_data['image1'])
    elif triage.valid_base64(infraction_data['image2']):
        dict_plates_identification = communication.search_plate(
                                                    infraction_data['image2'])
    else:
        LOGGER.error('INFO No valid images found! ending the function.')
        return None
    LOGGER.debug(f'result of search_plate: {dict_plates_identification}')
    communication.rdm_insert_audit(dict_plates_identification)

    plate = triage.extract_plate(dict_plates_identification)
    LOGGER.debug(f'result of extract_plate: {plate}')
    communication.rdm_insert_audit(plate)

    vehicle_data = communication.get_vehicle_info(plate)
    LOGGER.debug(f'result of get_vehicle_info: {vehicle_data}')
    communication.rdm_insert_audit(vehicle_data)

    LOGGER.info('Saving data on RDM')
    communication.rdm_insert_infraction(infraction_data, vehicle_data)

    LOGGER.info('Ending the actions for vehicle flagrant')
    pass


def _action_status_radar(radar_status_data):
    LOGGER.info('Starting the actions for radar\'s status')
    communication.rdm_insert_radar_status(radar_status_data)
    communication.rdm_insert_audit(radar_status_data)
    pass


dict_actions = {
    'vehicle-flagrant': _action_vehicle_flagrant,
    'status-radar': _action_status_radar
}


def select_action(dict_msg):
    try:
        type_msg = dict_msg['type']
    except:
        LOGGER.error('Error trying to identify the type of the message! No actions will be taken!')

    dict_actions[type_msg](dict_msg['payload'])
