import json
from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers=["10.129.150.90:9092"],
    value_serializer=lambda m: json.dumps(m).encode("ascii"),
)

msg = {
    "header": {
        "topicName": "TOP22_05_FACE_RECO_DONE",
        "topicVer1": 1,
        "topicVer2": 0,
        "msgId": "Message Id",
        "sender": "WAT",
        "sentUtc": "2020-11-05T14:12:17.5767851Z",
        "status": "System",
        "msgType": "Data",
        "source": "WAT Face recognition module",
        "scope": "Private",
        "caseId": "d5f97fe2-ab74-4ffd-8036-a3709f5953ae",
    },
    "body": {
        "camID": "Cam1234",
        "level": "high",
        "reason": "watch-list",
        "sourceURL": "https://www.crest.org/images/image1.jpg",
        "faceRecognized": {
            "dataStoreId": "5f22c0f20c0afda939169007",
            "subjectID": "Donald Duck",
            "subjectName": "suspect",
            "confidence": "0.789",
            "subjectDesc": "suspect recognized",
            "bbox": ["5 10 120 121"],
            "LeaURL": "https://www.crest.org/images/image1.jpg",
        },
        "timestamp": "1970-01-01 00:00:00",
    },
}


# Asynchronous by default
future = producer.send("TOP22_05_FACE_RECO_DONE", msg)

# Block for 'synchronous' sends
try:
    record_metadata = future.get(timeout=10)
except Exception:
    # Decide what to do if produce request failed...
    print("RE")
    pass
