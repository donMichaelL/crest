import json
from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers=["10.129.150.90:9092"],
    value_serializer=lambda m: json.dumps(m).encode("ascii"),
)

msg = {
   "header":{
      "topicName":"TOP22_08_ACTIVITY_RECO_DONE",
      "topicVer1":1,
      "topicVer2":2,
      "msgId":"Message Id",
      "sender":"CERTH",
      "sentUtc":"2022-11-10T08:04:01.973664Z",
      "status":"System",
      "msgType":"Data",
      "source":"CERTH Activity Recognition module",
      "scope":"Private",
      "caseId":"86b8b6bd42ce110000000900",
      "caseid":"0"
   },
   "body":{
      "deviceId":"cam-1",
      "domainId":"visualAnalysis:activityRecognition:dd4f82e5-7cbb-47c0-b31e-6fc3ea281f7b",
      "activityDetected":{
         "score":[
            0.9181
         ],
         "className":[
            "PersonStands"
         ],
         "classId":[
            2
         ],
         "activityDescription":[
            "A person is standing with at least one foot in contact with the ground and no net translation in movement for short time scales. Must be standing for a minimum of 2 s to add annotation."
         ],
         "activityDuration":[
            13.83
         ]
      },
      "timestampProcessing":"2022-11-10T08:04:01.973691Z",
      "mediaRootId":"/projects/86b8b6bd42ce110000000900/artefacts/636cb071bc62b2df22f797a7/media/111"
   }
}


# Asynchronous by default
future = producer.send("TOP22_08_ACTIVITY_RECO_DONE", msg)

# Block for 'synchronous' sends
try:
    record_metadata = future.get(timeout=10)
except Exception:
    # Decide what to do if produce request failed...
    print("RE")
    pass
