import consumer.queue_worker as worker
import caller.triage as triage
import caller.selector as selector

def start_symphony(body_msg):
    # receive the message from queue
    dict_msg = triage.parse_json_dict(body_msg)
    print(f'generated dictionary: {dict_msg}')

    # do the necessary actions based in the message type
    selector.select_action(dict_msg)


worker.main(start_symphony)
