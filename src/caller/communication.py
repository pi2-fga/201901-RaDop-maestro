import requests
import os
import uuid
import datetime
import asyncio
import json
import websockets
from websockets import ConnectionClosed
import logging

LOG_FORMAT = ('%(asctime)s %(levelname)10s - %(name)s %(funcName)s:\n%(message)s')
LOGGER = logging.getLogger(__name__)

ALPR_KEY = os.getenv('ALPR_KEY', '')
FN_HOST = os.getenv('FN_HOST', 'localhost')
FN_PORT = os.getenv('FN_PORT', 8080)
API_PORT = os.getenv('API_PORT', 3333)
SINESP_HOST = os.getenv('SINESP_HOST', 'localhost')
RDM_HOST = os.getenv('RDM_HOST', 'localhost')
RDM_PORT = os.getenv('RDM_PORT', 8765)

def _generate_id():
    identifier = str(uuid.uuid4())
    return identifier


def _get_time():
    time = datetime.datetime.utcnow()
    time = str(time.isoformat('T') + 'Z')
    return time


async def _connect_rdm(database, table, payload):
    response = None
    try:
        async with websockets.connect(
                f'ws://{RDM_HOST}:{RDM_PORT}/insert') as websocket:
            dict_data = {
                'id': _generate_id(),
                'type': 'rethink-manager-call',
                'payload': {
                    'database': database,
                    'table': table,
                    'data': payload
                },
                'time': _get_time()
            }

            await websocket.send(json.dumps(dict_data))

            logging.debug(f'Data sent: {dict_data}')

            response = await asyncio.wait_for(websocket.recv(), timeout=20)

            if response is None:
                raise Exception('No data received from RDM')
    except (asyncio.TimeoutError, ConnectionRefusedError) as err:
        LOGGER.error(exc_info=True)
    except ConnectionClosed as err:
        LOGGER.error(exc_info=True)
    except RuntimeError as err:
        LOGGER.error(exc_info=True)
    except Exception as err:
        LOGGER.error(exc_info=True)
    else:
        return response
        # pass


def _start_connection_rdm(database, table, payload):
    LOGGER.info(f'Starting the connection with RDM in table "{table}" from database "{database}"')
    response = None

    asyncio.set_event_loop(
        asyncio.new_event_loop()
    )
    try:
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(_connect_rdm(database, table, payload))
    except (asyncio.TimeoutError, ConnectionRefusedError) as err:
        LOGGER.error(exc_info=True)
    except ConnectionClosed as err:
        LOGGER.error(exc_info=True)
    except RuntimeError as err:
        LOGGER.error(exc_info=True)
    except Exception as err:
        LOGGER.error(exc_info=True)
    else:
        return response
    finally:
        asyncio.get_event_loop().stop()
        return response


def _rdm_insert_image_infraction(image):
    LOGGER.info('Starting to insert the image from infraction in RDM')
    response = None

    image_data = { 'image': image }
    response = _start_connection_rdm('IMAGES', 'infraction_images', image_data)
    response = json.loads(response)

    return response['response_message']['generated_keys'][0]


def search_plate(image_vehicle=None):
    LOGGER.info('Starting the search for the plate of the image')
    if image_vehicle:
        dict_json = {
            'id': _generate_id(),
            'type': 'alpr-call',
            'payload': {
                'key': ALPR_KEY,
                'image': image_vehicle
            },
            'time': _get_time()
        }

        response = requests.post(f'http://{FN_HOST}:{FN_PORT}/function/fn-alpr',
                                 json=dict_json)

        response_dict = response.json()

        if response.status_code == 200:
            return response.json()
        else:
            LOGGER.warning(f"The request wasn\'t sucessfull. Received status code {response.status_code}")
            return None

    else:
        LOGGER.error('No image was sent!')
        return None


def get_vehicle_info(plate=None):
    LOGGER.info('Starting the search for infos about the vehicle')
    if plate:
        requests.get(f'{SINESP_HOST}/sinesp/token/new')
        response = requests.get(f'{SINESP_HOST}/sinesp/placa/{plate}')
        LOGGER.debug('Done the POST to SINESP')

        if response.status_code == 200:
            return response.json()
        else:
            LOGGER.warning(f"The request wasn\'t sucessfull. Received status code {response.status_code}")
            return None

    else:
        LOGGER.error('No plate was sent!')
        return None


def notify_infraction(infraction_data, vehicle_data, infraction_id):
    LOGGER.info('Starting the notification of the infraction')

    dict_json = {
        'id': _generate_id(),
        'type': 'notify-infraction-call',
        'payload': {
            'infraction_id': infraction_id,
            'infraction_data': {
                'infraction_id': infraction_id,
                'id_radar': infraction_data['id_radar'],
                'infraction': infraction_data['infraction'],
                'vehicle_speed': infraction_data['vehicle_speed'],
                'considered_speed': infraction_data['considered_speed'],
                'max_allowed_speed': infraction_data['max_allowed_speed']
            },
            'vehicle_data': {
                'brand': vehicle_data['modelo'],
                'chassis': vehicle_data['chassi'],
                'city': vehicle_data['municipio'],
                'color': vehicle_data['cor'],
                'date': vehicle_data['data'],
                'model': vehicle_data['modelo'],
                'model_year': vehicle_data['anoModelo'],
                'plate': vehicle_data['placa'],
                'return_code': vehicle_data['codigoRetorno'],
                'return_message': vehicle_data['mensagemRetorno'],
                'state': vehicle_data['uf'],
                'status_code': vehicle_data['codigoSituacao'],
                'status_message': vehicle_data['situacao'],
                'year': vehicle_data['ano']
            }
        },
        'time': _get_time()
    }

    response = requests.post(f'http://{FN_HOST}:{FN_PORT}/function/fn-notify-infraction',
                                json=dict_json)

    if response.status_code == 200:
            return dict_json
    else:
        LOGGER.warning(f"The request wasn\'t sucessfull. Received status code {response.status_code}")
        return None


def notify_feasible(infraction_data, infraction_id):
    LOGGER.info('Starting the notification of the feasible')

    dict_json = {
        'id': _generate_id(),
        'type': 'notify-feasible-call',
        'payload': {
            'infraction_id': infraction_id,
            'infraction': infraction_data['infraction'],
            'vehicle_speed': infraction_data['vehicle_speed'],
            'considered_speed': infraction_data['considered_speed'],
            'max_allowed_speed': infraction_data['max_allowed_speed']
        },
        'time': _get_time()
    }

    response = requests.post(f'http://{FN_HOST}:{FN_PORT}/function/fn-notify-feasible',
                                json=dict_json)

    if response.status_code == 200:
            return dict_json
    else:
        LOGGER.warning(f"The request wasn\'t sucessfull. Received status code {response.status_code}")
        return None


def rdm_insert_infraction(infraction_data, vehicle_data):
    LOGGER.info('Starting to insert data about the infraction and vehicle in RDM')
    image_id1 = _rdm_insert_image_infraction(infraction_data['image1'])
    image_id2 = _rdm_insert_image_infraction(infraction_data['image2'])
    infraction = infraction_data
    infraction['image1'] = 'image_id1'
    infraction['image2'] = 'image_id2'
    infraction_id = _generate_id()

    insert_data = {
        'id': infraction_id,
        'type': 'radar-infraction',
        'payload': {
            'infraction_data': infraction,
            'vehicle_data': vehicle_data
        },
        'time': _get_time()
    }

    _start_connection_rdm('RADAR', 'infraction', insert_data)
    rdm_insert_audit(insert_data)

    return infraction_id


def rdm_insert_radar_status(radar_status_data):
    LOGGER.info('Starting to insert data about the radar\'s status in RDM')
    time = _get_time()
    insert_data = {
        'id': _generate_id(),
        'type': 'radar-app-data',
        'payload': radar_status_data,
        'time': time
    }

    api_data = radar_status_data
    api_data['date'] = time.rsplit('T')[0].replace('-', '/')
    api_data['time'] = time.rsplit('T')[1].rsplit('.')[0][:-3]
    LOGGER.debug('Sending data to API')
    requests.post(f'http://{FN_HOST}:{API_PORT}/radar/statuses/',
                                json=api_data)

    LOGGER.debug('Sending data to RDM')
    _start_connection_rdm('RADAR', 'status', insert_data)

    rdm_insert_audit(insert_data)
    rdm_insert_audit(api_data)


def rdm_insert_audit(payload):
    LOGGER.info('Sending data for Maestro\'s audition')
    insert_data = payload

    _start_connection_rdm('AUDIT', 'maestro', insert_data)
