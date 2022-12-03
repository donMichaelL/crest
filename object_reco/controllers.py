from settings import VEHICLE_COLOUR_LIST, FORBIDDEN_VEHICLE_CATEGORIES
from services.models import HandleKafkaTopic
from services.geo_services import check_server_for_restricted_area
from services.kafka_services import publish_to_kafka
from services.redis_services import write_list_to_redis
from services.ciram_services import post_ciram

from .models import ObjectDetectionEntity


class TOP22_02_OBJECT_RECO_DONE(HandleKafkaTopic):
    model = ObjectDetectionEntity

    def execute(self):
        super().execute()
        objects_msg = self.get_entities()
        object_descr = objects_msg.body.objectsDetected["description"]
        if objects_msg.header.sender == "NKUA":
            print(object_descr)
            return;

        for car_colour in VEHICLE_COLOUR_LIST:
            if car_colour in objects_msg.body.objectsDetected["description"]:
                write_list_to_redis("OD_CARS", (list(car_colour.split(" "))[1].lower()))

        _, _, area = check_server_for_restricted_area(objects_msg.body.deviceId)
        for vehicle in FORBIDDEN_VEHICLE_CATEGORIES:
            if vehicle in object_descr:
                objects_msg.body.objectsDetected["description"] = f"[NOT_ALLOWEDED_IN_AREA] ALERT in {area or 'a non restricted area'}: {vehicle} type is forbidden in that area."
                publish_to_kafka("TOP22_02_OBJECT_RECO_DONE", objects_msg.header.caseId, objects_msg.to_dict()["objectsDet"])
        post_ciram(objects_msg.custom_to_dict())
