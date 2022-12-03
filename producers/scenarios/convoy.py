import json
from kafka import KafkaProducer

from messages import COMMAND_MISSION, SUSPECT_PLATE, STOLEN_CAR, CONVOY_CAR, SUSPECT_EXIT, STOLEN_CAR_EXIT, CONVOY_CAR_EXIT

import time

producer = KafkaProducer(
    bootstrap_servers=["10.129.150.90:9092"],
    value_serializer=lambda m: json.dumps(m).encode("ascii"),
)

def send_to_kafka(topic, msg):
    # Asynchronous by default
    future = producer.send(topic, msg)

    # Block for 'synchronous' sends
    try:
        record_metadata = future.get(timeout=10)
    except Exception:
        # Decide what to do if produce request failed...
        print("RE")
        pass



send_to_kafka("TOP21_01_COMMAND_CENTER_MISSION", COMMAND_MISSION)

time.sleep(1)

send_to_kafka("TOP22_11_LPR_DONE", SUSPECT_PLATE)

time.sleep(1)

send_to_kafka("TOP22_11_LPR_DONE", CONVOY_CAR)

time.sleep(1)

send_to_kafka("TOP22_11_LPR_DONE", STOLEN_CAR)

time.sleep(2)

send_to_kafka("TOP22_11_LPR_DONE", SUSPECT_EXIT)

time.sleep(1)

send_to_kafka("TOP22_11_LPR_DONE", CONVOY_CAR_EXIT)

time.sleep(1)

send_to_kafka("TOP22_11_LPR_DONE", STOLEN_CAR_EXIT)
