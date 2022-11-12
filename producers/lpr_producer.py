import json
from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers=["10.129.150.90:9092"],
    value_serializer=lambda m: json.dumps(m).encode("ascii"),
)

msg = {
    "header": {
        "topicName": "TOP22_11_LPR_DONE",
        "topicVer1": 1,
        "topicVer2": 2,
        "msgId": "Message Id",
        "sender": "CERTH",
        "sentUtc": "2022-04-13T06:45:23.007783Z",
        "status": "System",
        "msgType": "Data",
        "source": "CERTH LPR module",
        "scope": "Private",
        "caseId": "6368e4cf9a91bd00019e7cf9",
    },
    "body": {
        "deviceId": "cam-15",
        "platesDetected": {
            "text": [
                "JSC2936",
            ],
            "boxes": [[300, 724, 168, 28]],
            "scores": [
                0.741867661476135,
            ],
            "url": [
                "/projects/6204e17818279f000142419d/artefacts/62567181629b4b0e45fbfb23/media/115",
                "/projects/6204e17818279f000142419d/artefacts/62567181629b4b0e45fbfb23/media/115"

            ],
            "car_id": [
                10915
            ],
            "timestamp": [
                "2022-04-03T09:19:56Z", "2022-04-03T09:19:56Z"
            ],
            "country": [
                "XX", "YY"
            ],
        },
        "lastDetection": "2022-04-13T06:51:37Z",
        "lastAccessAPI": "2022-04-13T06:51:37Z",
        "timestampProcessing": "2022-04-13T06:45:23.007863Z",
    },
}


# Asynchronous by default
future = producer.send("TOP22_11_LPR_DONE", msg)

# Block for 'synchronous' sends
try:
    record_metadata = future.get(timeout=10)
    print("Message was sent!")
except Exception:
    # Decide what to do if produce request failed...
    print("RE")
    pass
