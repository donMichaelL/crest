from ast import If
import requests
import json
from datetime import datetime
from abc import ABC, abstractmethod
from collections import defaultdict
from time import time

from models import ConvoyItem, ActivityRecoEntity, LPRMessageEntity, FaceDetectionEntity, ObjectDetectionEntity, CODDetectionEntity, AreaEntity, CameraEntity, LPR

from settings import FUSION_GEO, CONVOY_THRESHOLD
from utils import publish_to_kafka_person_lingering, publish_to_kafka_plates, post_ciram, write_data_to_redis, get_data_from_redis, publish_to_kafka_areas, check_server_for_restricted_area
from typing import List

Convoy_dict = defaultdict(ConvoyItem)


class HandleKafkaTopic(ABC):
    def __init__(self, msg):
        self.msg = msg

    def get_entities(self):
        return self.model.from_json(self.msg)
    
    @abstractmethod
    def execute(self):
        print(f"Message from {self.__class__.__name__} received.")


class TOP22_08_ACTIVITY_RECO_DONE(HandleKafkaTopic):
    model = ActivityRecoEntity

    def execute(self):
        super().execute()
        activity = self.get_entities()
        print(f"Description: {activity.body.activityDetected.activityDescription}")
        if activity.header.sender == "NKUA":
            return;

        _, _, area = check_server_for_restricted_area(activity.body.deviceId)
        description_lenght = len(activity.body.activityDetected.activityDescription)
        for index, detection in enumerate(activity.body.activityDetected.activityDuration):
            if detection > 2 and description_lenght > index:
                new_descr = f"ALERT in {area}: " + activity.body.activityDetected.activityDescription[index]
                activity.body.activityDetected.activityDescription[index] = new_descr
        publish_to_kafka_person_lingering(activity.header.caseId, activity.to_dict()["body"])


class TOP22_11_LPR_DONE(HandleKafkaTopic):
    model = LPRMessageEntity

    def _update_areas_capacity(self, areas: List[AreaEntity], plates: List[LPR]):
        for plate in plates:
            area = [area for area in areas if area.name == plate.area][0]
            if camera := get_data_from_redis(plate.detection.deviceID):
                licence_plate = plate.detection.platesDetected.text
                if CameraEntity.from_json(camera).is_cameraIn():
                    if licence_plate not in area.licensePlates:
                        area.add_vehicle(licence_plate)
                        area.add_circling_vehicle(licence_plate)
                        area._check_vehicle_circling(licence_plate)
                else:
                    if licence_plate in area.licensePlates:
                        area.remove_vehicle(licence_plate)
        write_data_to_redis("areas", AreaEntity.schema().dumps(areas, many=True))
        return areas

    def execute(self):
        super().execute()
        lpr_msg = self.get_entities()

        convoy = False
        convoy_item = Convoy_dict[lpr_msg.body.deviceId]
        current_timestamp = int(time()) // 60

        if current_timestamp - convoy_item.timestamp_in_min > CONVOY_THRESHOLD:
            convoy_item.timestamp_in_min = current_timestamp
            convoy_item.license_plates.clear()

        for plate in lpr_msg.plates_detected:
            convoy_item.license_plates.add(plate.detection.platesDetected.text)
        
        if len(convoy_item.license_plates) > 3:
            convoy = True

        for plate in lpr_msg.plates_detected:
            plate.convoy = convoy
            


        if stored_area := get_data_from_redis('areas'):
            areas = self._update_areas_capacity(
                AreaEntity.schema().loads(stored_area, many=True),
                lpr_msg.plates_detected
            )
            publish_to_kafka_areas(lpr_msg.header.caseId, AreaEntity.schema().dumps(areas, many=True))  
        post_ciram(lpr_msg.custom_to_dict())
        publish_to_kafka_plates(lpr_msg)


class TOP21_01_COMMAND_CENTER_MISSION(HandleKafkaTopic):
    def _publish_to_geo_areas(self):
        headers = {"Content-Type": "application/json"}
        try:
            _ = requests.post(FUSION_GEO + 'set-areas/' , data=self.msg, headers=headers)
            print(f'Message was sent to geo with cameras and areas')
        except requests.ConnectionError as err:
            print(err)

    def _store_areas(self, data_dict):
        areas = AreaEntity.schema().load(data_dict["body"]["mission"]["areas"], many=True)
        write_data_to_redis("areas", AreaEntity.schema().dumps(areas, many=True))
    
    def _store_cameras(self, data_dict):
        cameras= CameraEntity.schema().load(
                data_dict["body"]["mission"]["equipment"]["cameras"], many=True
        )
        [write_data_to_redis(camera.deviceId, camera.to_json()) 
            for camera in cameras if camera.areaInOut]

    def execute(self):
        super().execute()
        data_dict = json.loads(self.msg)
        self._store_areas(data_dict)
        self._store_cameras(data_dict)
        self._publish_to_geo_areas()


class TOP22_05_FACE_RECO_DONE(HandleKafkaTopic):
    model = FaceDetectionEntity

    def execute(self):
        super().execute()
        post_ciram(self.get_entities().custom_to_dict())


class TOP10_02_COD_ALERT(HandleKafkaTopic):
    model = CODDetectionEntity

    def execute(self):
        super().execute()
        post_ciram(self.get_entities().custom_to_dict())
    

class TOP22_02_OBJECT_RECO_DONE(HandleKafkaTopic):
    model = ObjectDetectionEntity

    def execute(self):
        super().execute()
        post_ciram(self.get_entities().custom_to_dict())


class TOP12_05_VEHICLE_COUNT_EVENT(HandleKafkaTopic):
    def execute(self):
        super().execute()
        print(json.loads(self.msg))


class TOP12_04_LPR_ALERT(HandleKafkaTopic):
    def execute(self):
        super().execute()
        print(f"Plate: {json.loads(self.msg)['body']['detection']['platesDetected']['text']} timestamp: {datetime.now()}")
        print(self.msg)

