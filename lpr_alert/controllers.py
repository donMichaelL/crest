import json

from datetime import datetime
from services.models import HandleKafkaTopic


class TOP12_04_LPR_ALERT(HandleKafkaTopic):
    def execute(self):
        # print(self.msg)
        super().execute()
        print(f"Plate: {json.loads(self.msg)['body']['detection']['platesDetected']['text']} timestamp: {datetime.now()}")
        print(f"DeviceId: {json.loads(self.msg)['body']['detection']['deviceId']}")
        print(f"Description: {json.loads(self.msg)['body']['description']}")

