import requests
import json
from collections import defaultdict
from time import time

from models import ConvoyItem, LPRMessageEntity, ObjectDetectionEntity, AreaEntity, CameraEntity, LPR

from settings import CONVOY_THRESHOLD, CONVOY_THRESHOLD_NUMBER, FORBIDDEN_VEHICLE_CATEGORIES, NATIONAL_DB_STOLEN, VEHICLE_COLOUR_LIST
from utils import publish_to_kafka_forbidden_vehicle, publish_to_kafka_plates, post_ciram, publish_to_kafka_areas, check_server_for_restricted_area
from services.redis_services import write_data_to_redis, get_data_from_redis
from services.models import HandleKafkaTopic

from typing import List

Convoy_dict = defaultdict(ConvoyItem)
OD_CARS = []


class TOP22_11_LPR_DONE(HandleKafkaTopic):
    model = LPRMessageEntity
    LPR_COLOR = ""

    def _update_areas_capacity(self, areas: List[AreaEntity], plates: List[LPR]):
        self.circling_plates = []
        for plate in plates:
            area = [area for area in areas if area.name == plate.area][0]
            if camera := get_data_from_redis(plate.detection.deviceID):
                licence_plate = plate.detection.platesDetected.text
                if CameraEntity.from_json(camera).is_cameraIn():
                    if licence_plate not in area.licensePlates:
                        area.add_vehicle(licence_plate)
                        area.add_circling_vehicle(licence_plate)
                        self.circling_plates.extend(area._check_vehicle_circling(licence_plate))
                else:
                    if licence_plate in area.licensePlates:
                        area.remove_vehicle(licence_plate)
        write_data_to_redis("areas", AreaEntity.schema().dumps(areas, many=True))
        return areas
    
    def _check_if_vehicle_stolen(self, plate) -> bool:
        response = requests.get(NATIONAL_DB_STOLEN + plate)
        try:
            msg = response.json()[0]
            self.LPR_COLOR = msg["color"]
            if msg['stolen'] == 'true':
                return True
            return False
        except Exception as err:
            return False

    def execute(self):
        super().execute()
        lpr_msg = self.get_entities()

        if stored_area := get_data_from_redis('areas'):
            areas = self._update_areas_capacity(
                AreaEntity.schema().loads(stored_area, many=True),
                lpr_msg.plates_detected
            )
            publish_to_kafka_areas(lpr_msg.header.caseId, AreaEntity.schema().dumps(areas, many=True))  

        convoy_item = Convoy_dict[lpr_msg.body.deviceId]
        current_timestamp = int(time()) // 60

        if current_timestamp - convoy_item.timestamp_in_min > CONVOY_THRESHOLD:
            convoy_item.timestamp_in_min = current_timestamp
            convoy_item.license_plates.clear()

        for plate in lpr_msg.plates_detected:
            convoy_item.license_plates.add(plate.detection.platesDetected.text)
        
        for plate in lpr_msg.plates_detected:
            if len(convoy_item.license_plates) > CONVOY_THRESHOLD_NUMBER:
                plate.description = f"Alert: Convoy. " + plate.description
            if plate.detection.platesDetected.text in self.circling_plates:
                plate.description = f"Alert: Returning vehicle. " + plate.description
            if self._check_if_vehicle_stolen(plate.detection.platesDetected.text):
                plate.description = f"Alert: Stolen vehicle. " + plate.description
            if len(OD_CARS) > 0 and self.LPR_COLOR not in OD_CARS:
                plate.description = f"Alert: Fake plate." + plate.description

        post_ciram(lpr_msg.custom_to_dict())
        publish_to_kafka_plates(lpr_msg)


class TOP22_02_OBJECT_RECO_DONE(HandleKafkaTopic):
    model = ObjectDetectionEntity

    def execute(self):
        super().execute()
        objects_msg = self.get_entities()
        object_descr = objects_msg.body.objectsDetected["description"]
        print(object_descr)
        if objects_msg.header.sender == "NKUA":
            return;

        OD_CARS.clear()

        for car_colour in VEHICLE_COLOUR_LIST:
            if car_colour in objects_msg.body.objectsDetected["description"]:
                OD_CARS.append(list(car_colour.split(" "))[1].lower())
        
        _, _, area = check_server_for_restricted_area(objects_msg.body.deviceId)
        for vehicle in FORBIDDEN_VEHICLE_CATEGORIES:
            if vehicle in object_descr:
                new_descr = f"ALERT {vehicle} is forbidden in {area}: " + objects_msg.body.objectsDetected["description"]
                objects_msg.body.objectsDetected["description"] = new_descr
                publish_to_kafka_forbidden_vehicle(objects_msg.header.caseId, objects_msg.to_dict()["objectsDet"])
        post_ciram(objects_msg.custom_to_dict())


class TOP12_05_VEHICLE_COUNT_EVENT(HandleKafkaTopic):
    def execute(self):
        super().execute()
        print(json.loads(self.msg))

