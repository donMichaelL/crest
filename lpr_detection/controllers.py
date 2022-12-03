from typing import List
from collections import defaultdict

from settings import CONVOY_THRESHOLD_NUMBER, CIRCLING_THRESHOLD_NUMBER
from services.models import HandleKafkaTopic
from services.redis_services import write_data_to_redis, get_data_from_redis, get_and_remove_list_from_redis
from services.ciram_services import post_ciram
from services.kafka_services import publish_to_kafka
from services.national_db_services import get_vehicle_attributes

from command_mission.models import AreaEntity, CameraEntity
from .models import LPRMessageEntity, LPR, ConvoyItem


class TOP22_11_LPR_DONE(HandleKafkaTopic):
    model = LPRMessageEntity
    convoy_dict = defaultdict(ConvoyItem)
    circling_plates = []

    def _update_areas_capacity(self, areas: List[AreaEntity], platesLPR: List[LPR]) -> List[AreaEntity]:
        self.circling_plates = []
        for plate in platesLPR:
            deviceId, licence_plate = plate.detection.deviceId, plate.detection.platesDetected.text
            if camera := CameraEntity.create_from_redis(deviceId):
                if area := next((area for area in areas if area.name == camera.area), None):
                    if camera.is_cameraIn():
                        if licence_plate not in area.licensePlates:
                            area.add_vehicle(licence_plate)
                            area.add_circling_vehicle(licence_plate)
                            self.circling_plates.extend(area._check_vehicle_circling(licence_plate))
                    else:
                        if licence_plate in area.licensePlates:
                            area.remove_vehicle(licence_plate)
        return areas
    
    def _calculate_vehicle_count(self, lpr_msg):
        if stored_area := get_data_from_redis('areas'):
            areas = self._update_areas_capacity(AreaEntity.schema().loads(stored_area, many=True), lpr_msg.plates_detected)
            publish_to_kafka("TOP12_05_VEHICLE_COUNT_EVENT", lpr_msg.header.caseId, {"areas": AreaEntity.schema().dump(areas, many=True)})
            write_data_to_redis("areas", AreaEntity.schema().dumps(areas, many=True))

    def execute(self):
        super().execute()
        lpr_msg = self.get_entities()

        self._calculate_vehicle_count(lpr_msg)

        convoy_item = self.convoy_dict[lpr_msg.body.deviceId]
        convoy_item.check_and_clear_licence_plates()
        convoy_item.add_licence_plates(lpr_msg.plates_detected)

        OD_CARS = get_and_remove_list_from_redis("OD_CARS")
        
        for plate in lpr_msg.plates_detected:
            plate_text = plate.detection.platesDetected.text
            self.color, self.stolen = get_vehicle_attributes(plate_text)
            area_name = plate.area if plate.area else "a non restricted area"
            if len(convoy_item.license_plates) >= CONVOY_THRESHOLD_NUMBER:                
                plate.description = f"[CONVOY] ALERT in {area_name}: A convoy of vehicles is entering the area. {convoy_item.license_plates} vehicles are entering the area in detected formation. The detected convoy fulfills the criterias for the vehicle count and the arrival proximity being small.\n" + plate.description
            if plate_text in self.circling_plates:
                plate.description = f"[RETURNING_VEHICLE] ALERT in {area_name}: Vehicle {plate_text} is detected suspiciously entering/leaving the area at least {CIRCLING_THRESHOLD_NUMBER} times! The vehicle is suspected of circling the designated area. Further actions for vehicle containment and further investigation is strongly advised.\n" + plate.description
            if self.stolen:
                plate.description = f"[STOLEN_CAR] ALERT in {area_name}: The system has the detected vehicle {plate_text} registered as stolen. Immidiate suspect vehicle containment is advised.\n" + plate.description
            if len(OD_CARS) > 0 and self.color not in OD_CARS:
                plate.description = f"[FAKE_PLATE] ALERT in {area_name}: There is a mismatch with the vehicle characteristics detected. The license plate must be fake. The system entry for the {self.color} vehicle {plate_text} does not mach the sensor detected characteristics.\n" + plate.description
            plate.vehicle["manufacturer"] = plate.description + plate.vehicle["manufacturer"]
            publish_to_kafka("TOP12_04_LPR_ALERT", lpr_msg.header.caseId, plate.to_dict())

        post_ciram(lpr_msg.custom_to_dict())
        