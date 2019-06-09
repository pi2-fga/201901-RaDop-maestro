import consumer.queue_worker as worker
import caller.triage as triage
import caller.selector as selector


def start_symphony(body_msg):
    dict_msg = triage.transform_json_payload(body_msg)

    selector.select_action(dict_msg)


worker.main(start_symphony)
