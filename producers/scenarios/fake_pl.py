import json
from kafka import KafkaProducer

from messages import COMMAND_MISSION, STOLEN_CAR, OBJECT_GRAY_CAR

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

send_to_kafka("TOP22_02_OBJECT_RECO_DONE", OBJECT_GRAY_CAR)

time.sleep(1)

send_to_kafka("TOP22_11_LPR_DONE", STOLEN_CAR)
