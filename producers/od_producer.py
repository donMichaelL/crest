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
    "sentUtc": "2022-05-19T13:12:47.343505Z",
    "status": "System",
    "msgType": "Data",
    "source": "CERTH Object detection module",
    "scope": "Private",
    "caseId": "0"
  },
  "body": {
    "deviceId": "cam-1",
    "domainId": "visualAnalysis:objectDetection:dbe39fab-7159-4bc6-8e25-78cb20877a23",
    "objectsDetected": {
      "boxes": [
        [
          131,
          155,
          63,
          28
        ],
        [
          179,
          113,
          70,
          158
        ],
        [
          240,
          95,
          80,
          173
        ]
      ],
      "scores": [
        0.967,
        0.996,
        0.965
      ],
      "classes": [
        2,
        0,
        0
      ],
      "class_names": [
        "car",
        "person",
        "person"
      ],
      "description": "truck 2 person(s),1 car(s) was/were detected. Vehicles type and color:car Gray"
    },
    "timestampProcessing": "2022-05-19T13:12:47.343533Z",
    "mediaRootId": "/projects/6204e17818279f000142419d/artefacts/628642403e29b525a7ae0e32/media/114"
  }
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
