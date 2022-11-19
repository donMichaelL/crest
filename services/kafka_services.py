import json

from datetime import datetime
from kafka import KafkaProducer

from settings import BOOTSTRAP_SERVER

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVER,
    value_serializer=lambda m: json.dumps(m).encode("ascii"),
)


def publishKafka(topic: str, header: dict, body: dict):
    future = producer.send(topic, {"header": header, "body": body})
    try:
        _ = future.get(timeout=10)
        print("Message was sent to Kafka!")
    except Exception:
        print("RE")
        pass

def publish_to_kafka_person_lingering(caseId, msg):
    header = {
        "topicName": "TOP22_08_ACTIVITY_RECO_DONE",
        "topicVer1": 1,
        "topicVer2": 0,
        "msgId": "Message Id",
        "sender": "NKUA",
        "sentUtc": datetime.utcnow().isoformat(),
        "status": "System",
        "msgType": "Alert",
        "source": "NKUA IoT Fusion module",
        "scope": "Private",
        "caseId": caseId,
    }
    publishKafka("TOP22_08_ACTIVITY_RECO_DONE", header, msg)

def publish_to_kafka_forbidden_vehicle(caseId, msg):
    header = {
        "topicName": "TOP22_02_OBJECT_RECO_DONE",
        "topicVer1": 1,
        "topicVer2": 0,
        "msgId": "Message Id",
        "sender": "NKUA",
        "sentUtc": datetime.utcnow().isoformat(),
        "status": "System",
        "msgType": "Alert",
        "source": "NKUA IoT Fusion module",
        "scope": "Private",
        "caseId": caseId,
    }
    publishKafka("TOP22_02_OBJECT_RECO_DONE", header, msg)

def publish_to_kafka_areas(caseId, areas):
    header = {
        "topicName": "TOP12_05_VEHICLE_COUNT_EVENT",
        "topicVer1": 1,
        "topicVer2": 0,
        "msgId": "Message Id",
        "sender": "NKUA",
        "sentUtc": datetime.utcnow().isoformat(),
        "status": "System",
        "msgType": "Alert",
        "source": "NKUA IoT Fusion module",
        "scope": "Private",
        "caseId": caseId,
    }
    publishKafka("TOP12_05_VEHICLE_COUNT_EVENT", header, {"areas": json.loads(areas)})

def publish_to_kafka_plates(lpr_message):
    header = {
        "topicName": "TOP12_04_LPR_ALERT",
        "topicVer1": 1,
        "topicVer2": 0,
        "msgId": "Message Id",
        "sender": "NKUA",
        "sentUtc": datetime.utcnow().isoformat(),
        "status": "System",
        "msgType": "Alert",
        "source": "NKUA IoT Fusion module",
        "scope": "Private",
        "caseId": lpr_message.header.caseId,
    }
    for plate in lpr_message.plates_detected:
        if hasattr(plate, "suspect"):
            # print(plate.to_dict())
            print(plate.to_dict())
            publishKafka("TOP12_04_LPR_ALERT", header, plate.to_dict())