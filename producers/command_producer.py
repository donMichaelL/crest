import json
from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers=["10.129.150.90:9092"],
    value_serializer=lambda m: json.dumps(m).encode("ascii"),
)

msg = {
   "header":{
      "topicName":"TOP21_01_COMMAND_CENTER_MISSION",
      "topicVer1":1,
      "topicVer2":0,
      "msgId":"CC-85453",
      "sender":"test-admin",
      "sentUtc":"2022-11-23T14:48:28.1643729Z",
      "status":"Test",
      "msgType":"Update",
      "source":"CC",
      "scope":"Restricted",
      "caseId":"637e27e8e1dabe00010eea96",
      "addresses":[
         
      ],
      "remotes":[
         
      ],
      "code":[
         
      ],
      "note":"",
      "references":[
         
      ]
   },
   "body":{
      "mission":{
         "id":"637e27e8e1dabe00010eea96",
         "status":"Plan",
         "settings":{
            "location":{
               "lat":44.47334,
               "lon":26.065527
            },
            "zoom":14,
            "name":"TEST_IOT_CC_221123",
            "authority":"TESTING",
            "status":"Enabled",
            "type":"Public",
            "accessUrl":"https://10.129.150.90:9099/app?MissionId=637e27e8e1dabe00010eea96",
            "description":"TEST_IOT_CC_221123",
            "startTime":"2022-11-23T14:01:53.000Z",
            "endTime":"2022-11-26T14:01:53.000Z"
         },
         "teams":[
            
         ],
         "equipment":{
            "cameras":[
               {
                  "name":"CAM 1",
                  "active":"false",
                  "type":"Fixed",
                  "status":"Low",
                  "deviceId":"cam-1",
                  "analytics":[
                     "LPR"
                  ],
                  "area":"AREA_01",
                  "areaInOut":"In",
                  "location":{
                     "lat":44.47248035224538,
                     "lon":26.065997532532315
                  }
               },
               {
                  "name":"CAM 2",
                  "active":"false",
                  "type":"Fixed",
                  "status":"Ready",
                  "deviceId":"cam-2",
                  "analytics":[
                     "LPR"
                  ],
                  "area":"AREA_01",
                  "areaInOut":"Out",
                  "location":{
                     "lat":44.47379227101999,
                     "lon":26.065304354857457
                  }
               }
            ]
         },
         "areas":[
            {
               "name":"AREA_01",
               "type":"Polygon",
               "vertices":[
                  {
                     "lat":44.473955806913104,
                     "lon":26.06481671333313
                  },
                  {
                     "lat":44.47219495449301,
                     "lon":26.065707206726078
                  },
                  {
                     "lat":44.472363386152864,
                     "lon":26.066554784774784
                  },
                  {
                     "lat":44.47412423349101,
                     "lon":26.0656213760376
                  }
               ]
            }
         ],
         "routes":[
            
         ]
      }
   }
}

# Asynchronous by default
future = producer.send("TOP21_01_COMMAND_CENTER_MISSION", msg)

# Block for 'synchronous' sends
try:
    record_metadata = future.get(timeout=10)
except Exception:
    # Decide what to do if produce request failed...
    print("RE")
    pass
