from typing import List
from collections import defaultdict

from settings import CONVOY_THRESHOLD_NUMBER, CIRCLING_THRESHOLD_NUMBER
from services.models import HandleKafkaTopic
from services.redis_services import write_data_to_redis, get_data_from_redis, get_and_remove_list_from_redis
from services.ciram_services import post_ciram
from services.kafka_services import publish_to_kafka_areas, publish_to_kafka_plates
from services.national_db_services import get_vehicle_attributes

from command_mission.models import AreaEntity, CameraEntity
from .models import LPRMessageEntity, LPR, ConvoyItem


class TOP22_11_LPR_DONE(HandleKafkaTopic):
    model = LPRMessageEntity
    convoy_dict = defaultdict(ConvoyItem)
    circling_plates = []

    def _update_areas_capacity(self, areas: List[AreaEntity], plates: List[LPR]):
        self.circling_plates = []
        for plate in plates:
            area = [area for area in areas if area.name == plate.area][0]
            if camera := get_data_from_redis(plate.detection.deviceId):
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
    
    def _create_vehicle_count_msg(self, lpr_msg):
        if stored_area := get_data_from_redis('areas'):
            areas = self._update_areas_capacity(
                AreaEntity.schema().loads(stored_area, many=True),
                lpr_msg.plates_detected
            )
            publish_to_kafka_areas(lpr_msg.header.caseId, AreaEntity.schema().dumps(areas, many=True))  

    def execute(self):
        super().execute()
        lpr_msg = self.get_entities()

        self._create_vehicle_count_msg(lpr_msg)

        convoy_item = self.convoy_dict[lpr_msg.body.deviceId]
        convoy_item.check_and_clear_licence_plates()
        convoy_item.add_licence_plates(lpr_msg.plates_detected)

        OD_CARS = get_and_remove_list_from_redis("OD_CARS")
        
        for plate in lpr_msg.plates_detected:
            plate_text = plate.detection.platesDetected.text
            self.color, self.stolen = get_vehicle_attributes(plate_text)
            if len(convoy_item.license_plates) > CONVOY_THRESHOLD_NUMBER:
                plate.description = f"ALERT in {plate.area}: A convoy of vehicles is entering a restricted area. {convoy_item.license_plates} vehicles are entering restricted area {plate.area} in detected formation. The detected convoy fulfills the criterias for the vehicle count and the arrival proximity being small." + plate.description
            if plate_text in self.circling_plates:
                plate.description = f"ALERT in {plate.area}: Vehicle {plate_text} is detected suspiciously entering/leaving restricted area {plate.area} at least {CIRCLING_THRESHOLD_NUMBER} times! The vehicle is suspected of circling the designated area. Further actions for vehicle containment and further investigation is strongly advised." + plate.description
            if self.stolen:
                plate.description = f"ALERT in {plate.area}: The system has the detected vehicle {plate_text} registered as stolen. Immidiate suspect vehicle containment is advised." + plate.description
            if len(OD_CARS) > 0 and self.color not in OD_CARS:
                plate.description = f"ALERT in {plate.area}: There is a mismatch with the vehicle characteristics detected. The license plate must be fake. The system entry for the {self.color} vehicle {plate_text} does not mach the sensor detected characteristics." + plate.description
            plate.vehicle["manufacturer"] = plate.description + plate.vehicle["manufacturer"]
        post_ciram(lpr_msg.custom_to_dict())
        print(lpr_msg.custom_to_dict())
        publish_to_kafka_plates(lpr_msg)