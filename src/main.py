import consumer.queue_worker as worker
import caller.triage as triage

def start_symphony(body_msg):
    dict_msg = triage.parse_json_dict(body_msg)
    print(f'generated dictionary: {dict_msg}')

worker.main(start_symphony)
