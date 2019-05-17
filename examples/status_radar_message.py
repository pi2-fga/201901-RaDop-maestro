# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0103,R0205

import json
import pika
import sys

EXCHANGE = 'message'
EXCHANGE_TYPE = 'topic'
QUEUE = 'maestro'
ROUTING_KEY = 'message.maestro'
HOST = 'localhost'

print('pika version: %s' % pika.__version__)

carga, temp, status_rasp, status_camera, status_rf, status_server = sys.argv[1:7]
print(sys.argv)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=HOST))
main_channel = connection.channel()

main_channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE)

msg = {
    "type": "status_radar",
    "payload": {
        "cargaBateria": carga,
        "temperatura": temp,
        "raspberry": status_rasp,
        "camera": status_camera,
        "rf": status_rf,
        "servidor": status_server
    }
}
main_channel.basic_publish(
    exchange=EXCHANGE,
    routing_key=ROUTING_KEY,
    body=json.dumps(msg),
    properties=pika.BasicProperties(content_type='application/json'))
print('send message %s' % msg)

connection.close()
