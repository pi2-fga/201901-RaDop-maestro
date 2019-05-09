import pika
import time

from triage import triage

ch_callback = None
method_callback = None

def callback(ch, method, properties, body):
    print('[X] nova mensagem recebida.')
    # send the message's body to be used by the orquestrator
    triage(body)

    print('[X] mensagem consumida. Enviando o ACK.')
    ch.basic_ack(delivery_tag = method.delivery_tag)

# create the connection and channel with the RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# create the queue in the RabbitMQ and configure it
channel.queue_declare(queue='task_queue', durable=True)
channel.basic_qos(prefetch_count=1)
# configure the consume of the messages from the queue
channel.basic_consume(
    queue='task_queue', on_message_callback=callback)

# start consuming the messages from queue
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
