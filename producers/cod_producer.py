import json
from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers=["10.129.150.90:9092"],
    value_serializer=lambda m: json.dumps(m).encode("ascii"),
)

msg = {
    "header": {
        "topicName": "TOP10_02_COD_ALERT",
        "topicVer1": 1,
        "topicVer2": 0,
        "msgId": "Message Id",
        "sender": "WAT",
        "sentUtc": "2020-11-05T20:44:11.7733705Z",
        "status": "System",
        "msgType": "Alert",
        "source": "WAT COD module",
        "scope": "Private",
        "caseId": "d5f97fe2-ab74-4ffd-8036-a3709f5953ae",
    },
    "body": {
        "device-ID": "COD-1",
        "imageURL": "https://www.crest.org/images/image1.jpg",
        "imageTHz": "https://www.crest.org/images/image2.jpg",
        "concealedObjects": [
            {
                "label": "Other",
                "prediction": 0.76,
                "size": "Small",
                "location": {"x": 0, "y": 0, "width": 100, "height": 100},
            },
            {
                "label": "Knife",
                "prediction": 0.76,
                "size": "Medium",
                "location": {"x": 10, "y": 10, "width": 100, "height": 100},
            },
            {
                "label": "Gun",
                "prediction": 0.76,
                "size": "Large",
                "location": {"x": 20, "y": 20, "width": 100, "height": 100},
            },
        ],
    },
}


# Asynchronous by default
future = producer.send("TOP10_02_COD_ALERT", msg)

# Block for 'synchronous' sends
try:
    record_metadata = future.get(timeout=10)
except Exception:
    # Decide what to do if produce request failed...
    print("RE")
    pass
