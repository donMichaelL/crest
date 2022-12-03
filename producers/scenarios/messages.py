OBJECT_GRAY_CAR = {
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
    "caseId": "637e27e8e1dabe00010eea96"
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
        ]
      ],
      "scores": [
        0.967,
      ],
      "classes": [
        2,
      ],
      "class_names": [
        "car",
      ],
      "description": "truck 2 person(s),1 car(s) was/were detected. Vehicles type and color:car Gray"
    },
    "timestampProcessing": "2022-05-19T13:12:47.343533Z",
    "mediaRootId": "/projects/6204e17818279f000142419d/artefacts/628642403e29b525a7ae0e32/media/114"
  }
}

CONVOY_CAR =  {
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
        "caseId": "637e27e8e1dabe00010eea96",
    },
    "body": {
        "deviceId": "cam-1",
        "platesDetected": {
            "text": [
                "CUSTOM",
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

CONVOY_CAR_EXIT =  {
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
        "caseId": "637e27e8e1dabe00010eea96",
    },
    "body": {
        "deviceId": "cam-2",
        "platesDetected": {
            "text": [
                "CUSTOM",
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

SUSPECT_EXIT =  {
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
        "caseId": "637e27e8e1dabe00010eea96",
    },
    "body": {
        "deviceId": "cam-2",
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

SUSPECT_PLATE = {
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
        "caseId": "637e27e8e1dabe00010eea96",
    },
    "body": {
        "deviceId": "cam-1",
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


STOLEN_CAR = {
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
        "caseId": "637e27e8e1dabe00010eea96",
    },
    "body": {
        "deviceId": "cam-1",
        "platesDetected": {
            "text": [
                "E65A851",
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

STOLEN_CAR_EXIT = {
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
        "caseId": "637e27e8e1dabe00010eea96",
    },
    "body": {
        "deviceId": "cam-2",
        "platesDetected": {
            "text": [
                "E65A851",
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


COMMAND_MISSION = {
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