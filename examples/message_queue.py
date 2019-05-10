import pika
import sys

# create the connection and channel with the RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# create the queue in the RabbitMQ and configure it
channel.exchange_declare(exchange='orquestrator', exchange_type='direct')
channel.queue_declare(queue='orquestrator_queue', durable=True)

## Use the code commented bellow to get the payload from command line
# message = ''.join(sys.argv[1:]).encode('utf-8')
message = '''
{
    "type": "message_type",
    "payload": {
        "number": 1234567890,
        "string": "some string",
        "boolean": false,
        "array": []
    }
}
'''

# configure the publisher of the messages from the queue
properties = pika.BasicProperties(
        content_type='application/json',
        content_encoding='utf-8',
        delivery_mode=2
    )

channel.basic_publish(
    exchange='',
    routing_key='orquestrator_queue',
    body=message,
    properties=properties
)

print('[x] Message sent to the queue. Closing the connection...')

connection.close()
