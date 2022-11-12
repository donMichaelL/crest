import json
from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers=["10.129.150.90:9092"],
    value_serializer=lambda m: json.dumps(m).encode("ascii"),
)

msg = {
	"header": {
		"topicName": "TOP21_01_COMMAND_CENTER_MISSION",
		"topicVer1": 1,
		"topicVer2": 0,
		"msgId": "CC-65376",
		"sender": "test",
		"sentUtc": "2021-05-10T12:40:12.7821556Z",
		"status": "Test",
		"msgType": "Update",
		"source": "CC",
		"scope": "Restricted",
		"caseId": "86b8b6bd42ce110000000900",
		"addresses": [],
		"remotes": [],
		"code": [],
		"note": "",
		"references": []
	},
	"body": {
		"mission": {
			"id": "86b8b6bd42ce110000000900",
			"status": "Plan",
			"settings": {
				"location": {
					"lat": 44.47328018177725,
					"lon": 26.065557003021244
				},
				"zoom": 18
			},
			"teams": [{
				"name": "Team 1",
				"status": "Active",
				"type": "Security",
				"leader": "Security 1",
				"location": {
					"lat": 44.472646656484535,
					"lon": 26.065728664398197
				},
				"units": [{
					"active": 'true',
					"name": "Security 1",
					"type": "Security",
					"bwcId": "bwc1",
					"argId": "agent1"
				}, {
					"active": 'true',
					"name": "Security 2",
					"type": "Security",
					"bwcId": "bwc2",
					"argId": "agent2"
				}, {
					"active": 'true',
					"name": "Security 3",
					"type": "Security",
					"bwcId": "bwc3",
					"argId": "agent3"
				}]
			}, {
				"name": "Team 2",
				"status": "Active",
				"type": "K9",
				"leader": "K9 1",
				"location": {
					"lat": 44.472520333398386,
					"lon": 26.066275835037235
				},
				"units": [{
					"active": 'true',
					"name": "K9 1",
					"type": "K9",
					"bwcId": "bwc6",
					"argId": "agent6",
					"phoneNumber": "0545567052",
					"profileImage": "http://18.185.14.210:8083/api/cases/86b8b6bd42ce110000000900/files/608020ec22778fb9282abec6/binary",
					"notes": "Note Example"
				}, {
					"active": 'true',
					"name": "K9 2",
					"type": "K9",
					"bwcId": "bwc7",
					"argId": "agent7"
				}, {
					"active": 'true',
					"name": "K9 3",
					"type": "K9",
					"bwcId": "bwc8",
					"argId": "agent8"
				}]
			}, {
				"name": "Team 3",
				"status": "Active",
				"type": "Mixed",
				"leader": "K9 4",
				"location": {
					"lat": 44.473844798221,
					"lon": 26.065449714660648
				},
				"units": [{
					"active": 'true',
					"name": "K9 4",
					"type": "K9",
					"bwcId": "bwc9",
					"argId": "agent9",
					"phoneNumber": "0545567052",
					"profileImage": "http://18.185.14.210:8083/api/cases/86b8b6bd42ce110000000900/files/60801f6422778fb9282a7a5a/binary",
					"notes": "Notes Test"
				}, {
					"active": 'true',
					"name": "K9 5",
					"type": "K9",
					"bwcId": "bwc10",
					"argId": "agent10"
				}, {
					"active": 'true',
					"name": "Security 4",
					"type": "Security",
					"bwcId": "bwc4",
					"argId": "agent4"
				}, {
					"active": 'true',
					"name": "Security 5",
					"type": "Security",
					"bwcId": "bwc5",
					"argId": "agent5"
				}]
			}, {
				"name": "Car 1",
				"status": "Active",
				"type": "Car",
				"leader": "K9 4",
				"location": {
					"lat": 44.47321667703834,
					"lon": 26.066981194050797
				},
				"units": [{
					"active": 'true',
					"name": "K9 1",
					"type": "K9",
					"bwcId": "bwc6",
					"argId": "agent6",
					"phoneNumber": "0545567052",
					"profileImage": "http://18.185.14.210:8083/api/cases/86b8b6bd42ce110000000900/files/608020ec22778fb9282abec6/binary",
					"notes": "Note Example"
				}, {
					"active": 'true',
					"name": "K9 2",
					"type": "K9",
					"bwcId": "bwc7",
					"argId": "agent7"
				}, {
					"active": 'true',
					"name": "K9 3",
					"type": "K9",
					"bwcId": "bwc8",
					"argId": "agent8"
				}, {
					"active": 'true',
					"name": "K9 4",
					"type": "K9",
					"bwcId": "bwc9",
					"argId": "agent9",
					"phoneNumber": "0545567052",
					"profileImage": "http://18.185.14.210:8083/api/cases/86b8b6bd42ce110000000900/files/60801f6422778fb9282a7a5a/binary",
					"notes": "Notes Test"
				}],
				"cameras": [{
					"url": "https://5e0d15ab12687.streamlock.net/live/MODIININDUSTRY.stream/chunklist_w1124728437.m3u8",
					"type": "RGB"
				}, {
					"url": "https://5d8c50e7b358f.streamlock.net/live/OFAKIM.stream/playlist.m3u8",
					"type": "RGB"
				}],
				"carType": "Sport",
				"motorcade": "Motorcade 1"
			}],
			"equipment": {
				"cameras": [{
					"name": "MODIININDUSTRY",
					"active": 'false',
					"type": "Fixed",
					"status": "Ready",
					"deviceId": "cam-1",
					"cameras": [{
						"url": "https://5e0d15ab12687.streamlock.net/live/MODIININDUSTRY.stream/chunklist_w104378689.m3u8",
						"type": "RGB"
					}],
					"location": {
						"lat": 44.473871593441885,
						"lon": 26.068518161773685
					},
					"analytics": ["OD", "FR", "AR", "CA", "LPR"],
					"area": "University",
					"areaInOut": "In"
				}, 
				{
					"name": "MODIININDUSTRY",
					"active": 'false',
					"type": "Fixed",
					"status": "Ready",
					"deviceId": "cam-15",
					"cameras": [{
						"url": "https://5e0d15ab12687.streamlock.net/live/MODIININDUSTRY.stream/chunklist_w104378689.m3u8",
						"type": "RGB"
					}],
					"location": {
						"lat": 44.473871593441885,
						"lon": 26.068518161773685
					},
					"analytics": ["OD", "FR", "AR", "CA", "LPR"],
					"area": "University",
					"areaInOut": "Out"
				}, 
				{
					"name": "ABUGOSH",
					"active": 'false',
					"type": "Fixed",
					"status": "Ready",
					"deviceId": "cam-2",
					"cameras": [{
						"url": "https://5e0d15ab12687.streamlock.net/live/ABUGOSH.stream/chunklist_w678205479.m3u8",
						"type": "RGB"
					}],
					"location": {
						"lat": 44.473545265093,
						"lon": 26.065404117107395
					},
					"analytics": ["OD", "FR", "AR", "CA"],
					"area": "University",
					"areaInOut": "Out"
				}, {
					"name": "OLGA",
					"active": 'false',
					"type": "Fixed",
					"status": "Ready",
					"deviceId": "cam-3",
					"cameras": [{
						"url": "https://5d8c50e7b358f.streamlock.net/live/OLGA.stream/chunklist_w883099480.m3u8",
						"type": "RGB"
					}],
					"location": {
						"lat": 44.47325,
						"lon": 26.069485
					},
					"analytics": ["OD", "FR", "AR"]
				}, {
					"name": "ALON",
					"active": 'false',
					"type": "Fixed",
					"status": "Moderate",
					"deviceId": "cam-4",
					"cameras": [{
						"url": "https://5e0d15ab12687.streamlock.net/live/ALON.stream/chunklist_w1593317748.m3u8",
						"type": "RGB"
					}],
					"location": {
						"lat": 44.47384097033131,
						"lon": 26.06926918029785
					},
					"analytics": ["OD", "FR"]
				}, {
					"name": "Pardasia",
					"active": 'false',
					"type": "Fixed",
					"status": "Moderate",
					"deviceId": "cam-5",
					"cameras": [{
						"url": "https://5e0d15ab12687.streamlock.net/live/PARDASIA.stream/chunklist_w1589570334.m3u8",
						"type": "RGB"
					}],
					"location": {
						"lat": 44.4750926768806,
						"lon": 26.070728302001957
					},
					"analytics": ["OD"]
				}],
				"uavs": [{
					"name": "UAV Test 1",
					"active": 'false',
					"type": "UAV",
					"status": "Ready",
					"deviceId": "cam-6",
					"cameras": [{
						"url": "https://5e0d15ab12687.streamlock.net/live/MODIININDUSTRY.stream/chunklist_w1124728437.m3u8",
						"type": "Thermal"
					}, {
						"url": "https://5d8c50e7b358f.streamlock.net/live/OFAKIM.stream/playlist.m3u8",
						"type": "IR"
					}],
					"area": "University",
					"location": {
						"lat": 44.47324472069795,
						"lon": 26.065893138759925
					}
				}, {
					"name": "UAV 10",
					"active": 'true',
					"type": "UAV",
					"status": "Ready",
					"deviceId": "cam-10",
					"location": {
						"lat": 44.47337587986406,
						"lon": 26.067042946815494
					}
				}],
				"ugvs": [{
					"name": "UGV Test 1",
					"active": 'false',
					"type": "UGV",
					"status": "Ready",
					"deviceId": "cam-7",
					"cameras": [{
						"url": "url 1",
						"type": "RGB"
					}, {
						"url": "url 2",
						"type": "RGB"
					}],
					"area": "CamPolygon",
					"location": {
						"lat": 44.473946,
						"lon": 26.068644
					}
				}, {
					"name": "TestRequired",
					"active": 'true',
					"type": "UGV",
					"status": "Ready",
					"deviceId": "cam-9",
					"location": {
						"lat": 44.473417986972535,
						"lon": 26.066651344299316
					}
				}],
				"cods": [{
					"name": "COD Test 1",
					"active": 'false',
					"type": "COD",
					"status": "Ready",
					"deviceId": "cam-8",
					"cameras": [{
						"url": "url1",
						"type": "RGB"
					}, {
						"url": "url2",
						"type": "RGB"
					}],
					"location": {
						"lat": 44.47417782366385,
						"lon": 26.067944169044498
					}
				}]
			},
			"areas": [{
				"name": "University",
				"type": "Polygon",
				"vertices": [{
					"lat": 44.47405533176792,
					"lon": 26.06489181518555
				}, {
					"lat": 44.47246291372338,
					"lon": 26.065750122070316
				}, {
					"lat": 44.47256244112414,
					"lon": 26.066034436225895
				}, {
					"lat": 44.47245525776243,
					"lon": 26.066104173660282
				}, {
					"lat": 44.47271173190707,
					"lon": 26.067257523536686
				}, {
					"lat": 44.47291844159141,
					"lon": 26.06715559959412
				}, {
					"lat": 44.472776807257034,
					"lon": 26.06657087802887
				}, {
					"lat": 44.47418547939884,
					"lon": 26.065868139266968
				}]
			}, {
				"name": "Parking",
				"type": "Polygon",
				"vertices": [{
					"lat": 44.474116577748035,
					"lon": 26.06857180595398
				}, {
					"lat": 44.474499363667505,
					"lon": 26.068507432937626
				}, {
					"lat": 44.47478262363142,
					"lon": 26.070202589035038
				}, {
					"lat": 44.47466013300493,
					"lon": 26.07065320014954
				}, {
					"lat": 44.47352708252136,
					"lon": 26.0711681842804
				}, {
					"lat": 44.473044763815864,
					"lon": 26.067852973937992
				}, {
					"lat": 44.473925183846724,
					"lon": 26.067498922348026
				}, {
					"lat": 44.47410892200404,
					"lon": 26.06857180595398
				}]
			}, {
				"name": "UAV Area",
				"type": "Circle",
				"center": {
					"lat": 44.47344286843143,
					"lon": 26.066983938217167
				},
				"radius": 50.290610988675596
			}],
			"routes": [{
				"vertices": [{
					"lat": 44.474,
					"lon": 26.0648
				}, {
					"lat": 44.474,
					"lon": 26.0648
				}, {
					"lat": 44.474,
					"lon": 26.0648
				}, {
					"lat": 44.474,
					"lon": 26.0648
				}],
				"name": "Route 1",
				"type": "Main"
			}, {
				"vertices": [{
					"lat": 44.474,
					"lon": 26.0648
				}, {
					"lat": 44.474,
					"lon": 26.0648
				}, {
					"lat": 44.474,
					"lon": 26.0648
				}, {
					"lat": 44.474,
					"lon": 26.0648
				}],
				"name": "Route 2",
				"type": "Alternative"
			}, {
				"vertices": [{
					"lat": 44.474,
					"lon": 26.0648
				}, {
					"lat": 44.474,
					"lon": 26.0648
				}, {
					"lat": 44.474,
					"lon": 26.0648
				}, {
					"lat": 44.474,
					"lon": 26.0648
				}],
				"name": "Route 3",
				"type": "Alternative"
			}, {
				"vertices": [{
					"lat": 44.474,
					"lon": 26.0648
				}, {
					"lat": 44.474,
					"lon": 26.0648
				}, {
					"lat": 44.474,
					"lon": 26.0648
				}, {
					"lat": 44.474,
					"lon": 26.0648
				}],
				"name": "Route 4",
				"type": "Alternative"
			}]
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
