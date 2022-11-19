import json

from services.models import HandleKafkaTopic


class TOP12_05_VEHICLE_COUNT_EVENT(HandleKafkaTopic):
    def execute(self):
        super().execute()
        print(json.loads(self.msg))