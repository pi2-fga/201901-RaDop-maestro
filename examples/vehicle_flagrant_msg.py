# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0103,R0205
import json
import pika
import sys
import uuid

EXCHANGE = 'message'
EXCHANGE_TYPE = 'topic'
QUEUE = 'maestro'
ROUTING_KEY = 'message.maestro'
HOST = 'localhost'


# test values: 65 2019-04-27T10:14:35Z 1 80 77 60 true image1, image2
# id_radar, time, infraction, vehicle_speed, considered_speed, max_allowed_speed, penality, image1, image2 = sys.argv[1:11]


def _generate_id():
    identifier = str(uuid.uuid4())
    return identifier


def send_vehicle_flagrant_msg(dict_msg):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=HOST))
    main_channel = connection.channel()

    main_channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE)

    uuid = _generate_id()
    msg = {
        "type": "vehicle-flagrant",
        "id": uuid,
        "time": dict_msg['time'],
        "payload": {
            "image1": dict_msg['image1'],
            "image2": dict_msg['image2'],
            "id_radar": dict_msg['id_radar'],
            "infraction": dict_msg['infraction'],
            "vehicle_speed": dict_msg['vehicle_speed'],
            "considered_speed": dict_msg['considered_speed'],
            "max_allowed_speed": dict_msg['max_allowed_speed'],
            "penality": dict_msg['penality']
        }
    }

    main_channel.basic_publish(
        exchange=EXCHANGE,
        routing_key=ROUTING_KEY,
        body=json.dumps(msg),
        properties=pika.BasicProperties(content_type='application/json'))
    print('send message %s' % msg)

    connection.close()
