import pika
import time

from triage import triage

ch_callback = None
method_callback = None

def callback(ch, method, properties, body):
    print('[X] New message received.')
    # send the message's body to be used by the orquestrator
    triage(body)

    print('[X] Message consumed. Sending the ACK back to the queue...')
    ch.basic_ack(delivery_tag = method.delivery_tag)

# create the connection and channel with the RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# create the queue in the RabbitMQ and configure it
channel.exchange_declare(exchange='orquestrator', exchange_type='direct')
channel.queue_declare(queue='orquestrator_queue', durable=True)
channel.basic_qos(prefetch_count=1)

# configure the consumer of the messages from the queue
channel.basic_consume(
    queue='orquestrator_queue', on_message_callback=callback)

# start consuming the messages from queue
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
