import json
from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers=["10.129.150.90:9092"],
    value_serializer=lambda m: json.dumps(m).encode("ascii"),
)

msg = {
    "header": {
        "topicName": "TOP22_02_OBJECT_RECO_DONE",
        "topicVer1": 1,
        "topicVer2": 2,
        "msgId": "Message Id",
        "sender": "CERTH",
        "sentUtc": "2021-04-26 13:06:49.874281",
        "status": "System",
        "msgType": "Data",
        "source": "CERTH Object detection module",
        "scope": "Private",
        "caseId": "60867cbf857aba00016b01e9",
    },
    "body": {
        "deviceId": "cam-11",
        "domainId": "visualAnalysis:objectDetection:46f49f30-8fc8-4156-864d-d01b8771b2af",
        "objectsDetected": {
            "boxes": [[209, 442, 347, 653], [267, 331, 388, 516]],
            "scores": [0.960647702217102, 0.5],
            "classes": [1, 2],
            "class_names": [
                "handbag",
            ],
            "description": "2 object(s) was/were detected",
        },
        "timestampProcessing": "2021-04-26 13:06:49.874292",
        "mediaRootId": "/projects/60867cbf857aba00016b01e9/artefacts/6086bae9171cd388734c7dcf/media",
    },
}


# Asynchronous by default
future = producer.send("TOP22_02_OBJECT_RECO_DONE", msg)

# Block for 'synchronous' sends
try:
    record_metadata = future.get(timeout=10)
except Exception:
    # Decide what to do if produce request failed...
    print("RE")
    pass
