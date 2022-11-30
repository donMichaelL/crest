from services.kafka_services import publish_to_kafka
from services.geo_services import check_server_for_restricted_area
from services.models import HandleKafkaTopic
from settings import PERSON_LINGERING_THRESHOLD

from .models import ActivityRecoEntity

import time

class TOP22_08_ACTIVITY_RECO_DONE(HandleKafkaTopic):
    model = ActivityRecoEntity

    def execute(self):
        super().execute()
        activity = self.get_entities()
        if activity.header.sender == "NKUA":
            print(f"Description: {activity.body.activityDetected.activityDescription}")
            return
        
        time.sleep(1)

        _, _, area = check_server_for_restricted_area(activity.body.deviceId)
        description_lenght = len(activity.body.activityDetected.activityDescription)
        found_alert = False
        for index, className in enumerate(activity.body.activityDetected.className):
            if className == "PersonStands":
                if activity.body.activityDetected.activityDuration[index] > PERSON_LINGERING_THRESHOLD and description_lenght > index:
                    found_alert = True
                    new_descr = f"ALERT in a non restricted area: A person is detected lingering. This bahaviour is deemed suspicious and further actions are advised."
                    if area:
                        new_descr = f"ALERT in {area}: A person is detected lingering inside the restricted area {area}. This bahaviour is deemed suspicious and further actions are advised."
                    activity.body.activityDetected.activityDescription[index] = new_descr
        if found_alert:
            publish_to_kafka("TOP22_08_ACTIVITY_RECO_DONE", activity.header.caseId, activity.to_dict()["body"])
