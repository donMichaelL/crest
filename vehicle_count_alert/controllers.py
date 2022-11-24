import json

from services.models import HandleKafkaTopic


class TOP12_05_VEHICLE_COUNT_EVENT(HandleKafkaTopic):
    def execute(self):
        # print(self.msg)
        super().execute()
        for area in json.loads(self.msg)['body']['areas']:
            print(f"Area: {area['name']} VehiclesIn: {area['vehiclesIn']} VehicleCount: {area['vehicleCount']} VehicleOut: {area['vehiclesOut']}")
