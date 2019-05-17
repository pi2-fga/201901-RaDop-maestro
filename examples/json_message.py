# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0103,R0205

import json
import pika

EXCHANGE = 'message'
EXCHANGE_TYPE = 'topic'
QUEUE = 'maestro'
ROUTING_KEY = 'message.maestro'

print('pika version: %s' % pika.__version__)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
main_channel = connection.channel()

main_channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE)

temp = 23

msg = {
    "type": "status_radar",
    "payload": {
        "cargaBateria": "42",
        "temperatura": temp,
        "raspberry": 1,
        "camera": 1,
        "rf": 1,
        "servidor": 1
    }
}
main_channel.basic_publish(
    exchange=EXCHANGE,
    routing_key=ROUTING_KEY,
    body=json.dumps(msg),
    properties=pika.BasicProperties(content_type='application/json'))
print('send message %s' % msg)

connection.close()
