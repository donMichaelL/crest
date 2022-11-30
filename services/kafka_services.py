import json

from datetime import datetime
from kafka import KafkaProducer

from settings import BOOTSTRAP_SERVER

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVER,
    value_serializer=lambda m: json.dumps(m).encode("ascii"),
)

def publish_to_kafka(topic: str, caseId: str, msg: dict):
    header = {
        "topicName": topic,
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

    future = producer.send(topic, {"header": header, "body": msg})
    try:
        _ = future.get(timeout=10)
        print(f"<<<< Message in topic: {topic} was sent to Kafka!")
    except Exception:
        print("RE")
        pass
 