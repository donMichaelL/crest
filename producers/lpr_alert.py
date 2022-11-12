import json
from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers=["10.129.150.90:9092"],
    value_serializer=lambda m: json.dumps(m).encode("ascii"),
)

msg = {
  "header": {
    "topicName": "TOP12_04_LPR_ALERT ",
    "topicVer1": 1,
    "topicVer2": 0,
    "msgId": "Message Id",
    "sender": "NKUA",
    "sentUtc": "2020-07-30T12:45:35+0000",
    "status": "System",
    "msgType": "Alert",
    "source": "NKUA IoT Fusion module",
    "scope": "Private",
    "caseId": "d5f97fe2-ab74-4ffd-8036-a3709f5953ae"
  },
  "body": {
  "detection": {
    "deviceId": "cam-22-lpr",
    "platesDetected": {
      "text": "JSC2936",
      "scores": 0.741867661476135,
      "url": "/projects/6204e17818279f000142419d/artefacts/62567181629b4b0e45fbfb23/media/115",
      "car_id": 10915,
      "timestamp": [
        "2022-04-13T06:51:37Z"
      ],
      "country": [
        "XX"
      ]
    }
  },
  "suspect": {
    "id": 5,
    "firstName": "Guenter",
    "lastName": "Seifert",
    "nickname": "gseif80",
    "age": 33,
    "lastKnownAddress": "001 Dovie Mount Apt. 251 Beckerstad, MD 84241",
    "profession": "",
    "email": "jameson.beahan@example.org",
    "photo": ".\\\\fakepath\\Photo5.jpg"
  },
  "vehicle": {
    "id": 6652,
    "manufacturer": "Chevrolet",
    "model": "consectetur",
    "color": "blue",
    "type": "SUV",
    "vin": "4N8IB13L9V8415995",
    "year": 1981,
    "licenseState": "Idaho",
    "licenseNumber": "JSC2936",
    "icon": ".\\\\fakepath\\Photo6652.jpg",
    "description": "",
    "registeredOwner": "Prof. Hazle Gusikowski PhD"
  },
  "severity": "Low"
}
}



# Asynchronous by default
future = producer.send("TOP12_04_LPR_ALERT", msg)

# Block for 'synchronous' sends
try:
    record_metadata = future.get(timeout=10)
    print("Message was sent!")
except Exception:
    # Decide what to do if produce request failed...
    print("RE")
    pass
