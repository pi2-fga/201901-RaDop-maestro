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

# test values: 65 58 1F C 7E4 17 3B 3B -3 4AAQSkZJRgABAQAAAQABAAD/wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL//2Q==
id_radar, speed, day, month, year, hour, minute, second, time_zone, image = sys.argv[1:11]

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=HOST))
main_channel = connection.channel()

main_channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE)

msg = {
    "type": "vehicle_flagrant",
    "payload": {
        "id_radar": id_radar,
        "speed": speed,
        "day": day,
        "month": month,
        "year": year,
        "hour": hour,
        "minute": minute,
        "second": second,
        "time-zone": time_zone,
        "image": image
    }
}
main_channel.basic_publish(
    exchange=EXCHANGE,
    routing_key=ROUTING_KEY,
    body=json.dumps(msg),
    properties=pika.BasicProperties(content_type='application/json'))
print('send message %s' % msg)

connection.close()
