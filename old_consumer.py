import json
from kafka import KafkaConsumer
from random import random
from datetime import datetime

from settings import BOOTSTRAP_SERVER, KAFKA_TOPICS, OFFSET_RESET
from models import LPRMessage, ODMessage, CODMessage, FDMessage, Mission
from utils import publish_to_kafka_plates, publish_to_ciram, publish_to_geo_areas


consumer = KafkaConsumer(
    group_id=str(random()),
    auto_offset_reset=OFFSET_RESET,
    bootstrap_servers=BOOTSTRAP_SERVER,
)
consumer.subscribe(KAFKA_TOPICS)


def main() -> None:
    print("Consumer is running....")
    for message in consumer:
        # print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value))
        topic = message.topic
        value = message.value

        if topic == "TOP12_05_VEHICLE_COUNT_EVENT":
            print(json.loads(value))

        if topic == "TOP22_11_LPR_DONE":
            lpr_message = LPRMessage.create_lpr_msg(json.loads(value))
            publish_to_kafka_plates(lpr_message)
            publish_to_ciram(lpr_message.to_ciram())

        if topic == "TOP12_04_LPR_ALERT":
            print('A message from TOP12_04_LPR_ALERT Received')
            print(f"Plate: {json.loads(value)['body']['detection']['platesDetected']['text']} timestamp: {datetime.now()}")
            print(json.loads(value))

        if topic == "TOP22_02_OBJECT_RECO_DONE":
            od = ODMessage.create_od_msg(json.loads(value))
            publish_to_ciram(od.__repr__())

        if topic == "TOP10_02_COD_ALERT":
            cod = CODMessage.create_cod_msg(json.loads(value))
            publish_to_ciram(cod.__repr__())

        if topic == "TOP22_05_FACE_RECO_DONE":
            fd = FDMessage.create_fd_msg(json.loads(value))
            publish_to_ciram(fd.__repr__())
        
        if topic == "TOP21_01_COMMAND_CENTER_MISSION":
            msg = json.loads(value)
            Mission.set_case_id(msg)
            publish_to_geo_areas(msg)

if __name__ == "__main__":
    main()




class LPRold:
    def __init__(self, device_id, text, score, url, car_id, timestamp, country):
        self.detection = {
            "deviceID": device_id,
            "platesDetected": {
                "text": text,
                "score": score,
                "url": url,
                "car_id": car_id,
                "timestamp": [timestamp],
                "country": [country],
            },
        }
        self.get_info_from_db()
        self.check_if_restricted_area()
        

    def __repr__(self) -> str:
        return str(self.__dict__)
    
    def check_if_restricted_area(self):
        self.severity, self.description = check_server_for_restricted_area(self.detection['deviceID'])

    def get_info_from_db(self):
        text = self.detection["platesDetected"]["text"]
        response = requests.get(NATIONAL_DB_URL + text)
        try:
            suspect_dict = response.json()[0]
            self.suspect = {
                key: suspect_dict[key]
                for key in suspect_dict.keys() & SUSPECT_ATTRS_SET
            }
            for vehicle in suspect_dict["vehicles"]:
                if vehicle["vehicleDetails"]["licenseNumber"] == text:
                    vehicles_dict = vehicle["vehicleDetails"]
                    self.vehicle = {
                        key: vehicles_dict[key]
                        for key in vehicles_dict.keys() & VEHICLE_ATTRS_SET
                    }
        except Exception as err:
            print(str(err))

class LPRMessage:
    def __init__(self, case_id, device_id, platesDetected):
        self.case_id = case_id
        self.device_id = device_id
        self.platesDetected = platesDetected

    def __repr__(self) -> str:
        return str(self.__dict__)
    
    def to_ciram(self) -> str:
        return str({
            "LPR": self.__dict__
        })

    @classmethod
    def create_lpr_msg(cls, json_value):
        case_id = "14"
        device_id = json_value["body"]["deviceId"]
        plates_detected = json_value["body"]["platesDetected"]
        platesDetected = []

        for index, value in enumerate(plates_detected["text"]):
            if plates_detected["scores"][index] >= 0.7:
                platesDetected.append(
                    LPRold(
                        device_id,
                        value.replace(' ', '%20'),
                        plates_detected["scores"][index],
                        (plates_detected["url"][index: ]+[''])[0],
                        (plates_detected["car_id"][index: ]+[''])[0],
                        (plates_detected["timestamp"][index: ]+[''])[0],
                        (plates_detected["country"][index: ]+[''])[0],
                    )
                )

        return LPRMessage(case_id, device_id, platesDetected)




