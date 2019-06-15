import consumer.queue_worker as worker
# import consumer.simple_consume_worker as simple_worker
import caller.triage as triage
import caller.selector as selector
import logging

LOG_FORMAT = ('%(asctime)s %(levelname)10s - %(name)s %(funcName)s:\n%(message)s')
LOGGER = logging.getLogger(__name__)

def start_symphony(body_msg):
    LOGGER.info('Starting the symphony')
    dict_msg = triage.transform_json_payload(body_msg)

    selector.select_action(dict_msg)


worker.main(start_symphony)
