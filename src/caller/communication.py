import requests
import os
import uuid
import datetime
import asyncio
import json
import websockets
from websockets import ConnectionClosed
import logging

LOG_FORMAT = ('%(levelname)s %(asctime)s - %(name)s %(funcName)s:\n%(message)s')
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
LOGGER = logging.getLogger(__name__)

ALPR_KEY = os.getenv('ALPR_KEY', '')
ALPR_HOST = os.getenv('ALPR_HOST', 'localhost')
ALPR_PORT = os.getenv('ALPR_PORT', 8080)
SINESP_DOMAIN = os.getenv('SINESP_DOMAIN', '')
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
        pass


def _start_connection_rdm(database, table, payload):
    LOGGER.info(f'Starting the connection with RDM in table "{table}" from database "{database}"')
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_connect_rdm(database, table, payload))
    except (asyncio.TimeoutError, ConnectionRefusedError) as err:
        LOGGER.error(exc_info=True)
    except ConnectionClosed as err:
        LOGGER.error(exc_info=True)
    except RuntimeError as err:
        LOGGER.error(exc_info=True)
    except Exception as err:
        LOGGER.error(exc_info=True)
    finally:
        asyncio.get_event_loop().stop()


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

        response = requests.post(f'http://{ALPR_HOST}:{ALPR_PORT}/function/fn-alpr',
                                 json=dict_json)

        response_dict = response.json()

        if response_dict['status_code'] == 200:
            return response_dict
        else:
            LOGGER.warning(f"The request wasn\'t sucessfull. Received status code {response_dict['status_code']}")
            return None

    else:
        LOGGER.error('No image was sent!')
        return None


def get_vehicle_info(plate=None):
    LOGGER.info('Starting the search for infos about the vehicle')
    if plate:
        uuid = _generate_id()
        time = _get_time()
        dict_json = {
            'id': uuid,
            'type': 'sinesp-call',
            'payload': {
                'plate': plate
            },
            'time': time
        }

        response = requests.post(f'http://{SINESP_DOMAIN}/function/fn-sinesp',
                                 json=dict_json)

        response_dict = response.json()
        if response_dict['status_code'] == 200:
            return response_dict['response']
        else:
            LOGGER.warning(f"The request wasn\'t sucessfull. Received status code {response_dict['status_code']}")
            return None

    else:
        LOGGER.error('No plate was sent!')
        return None


def rdm_insert_infraction(infraction_data, vehicle_data):
    LOGGER.info('Starting to insert data about the infraction and vehicle in RDM')
    insert_data = {
        'id': _generate_id(),
        'type': 'radar-infraction',
        'payload': {
            'infraction-data': infraction_data,
            'vehicle-data': vehicle_data
        },
        'time': _get_time()
    }

    _start_connection_rdm('RADAR', 'infraction', insert_data)
    # rdm_insert_audit(insert_data)


def rdm_insert_radar_status(radar_status_data):
    LOGGER.info('Starting to insert data about the radar\'s status in RDM')
    insert_data = {
        'id': _generate_id(),
        'type': 'radar-app-data',
        'payload': radar_status_data,
        'time': _get_time()
    }

    _start_connection_rdm('RADAR', 'status', insert_data)
    # rdm_insert_audit(insert_data)


def rdm_insert_audit(payload):
    LOGGER.info('Sending data for Maestro\'s audition')
    insert_data = payload

    _start_connection_rdm('AUDIT', 'maestro', insert_data)
