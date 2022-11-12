import json
from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers=["10.129.150.90:9092"],
    value_serializer=lambda m: json.dumps(m).encode("ascii"),
)

msg = {
    "header": {
      "topicName": "TOP12_05_VEHICLE_COUNT_EVENT",
      "topicVer1": 1,
      "topicVer2": 0,
      "msgId": "Message Id",
      "sender": "NKUA",
      "sentUtc": "2020-07-30T12:45:35+0000",
      "status": "System",
      "msgType": "Alert",
      "source": "NKUA IoT Fusion module",
      "scope": "Private",
      "caseId": "6204e17818279f000142419d"
    },
    "body":{
        "areas":[{
            "name": "University",
            "vehiclesIn": 5,
            "vehiclesOut": 4,
            "vehicleCount": 1,
            "licensePlates": ["JSC23936"]
        }]
    }
}

# Asynchronous by default
future = producer.send("TOP12_05_VEHICLE_COUNT_EVENT", msg)

# Block for 'synchronous' sends
try:
    record_metadata = future.get(timeout=10)
except Exception:
    # Decide what to do if produce request failed...
    print("RE")
    pass
