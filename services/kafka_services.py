from datetime import datetime

from utils import publishKafka

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