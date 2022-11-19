from services.models import HandleKafkaTopic
from services.ciram_services import post_ciram

from .models import CODDetectionEntity

class TOP10_02_COD_ALERT(HandleKafkaTopic):
    model = CODDetectionEntity

    def execute(self):
        super().execute()
        post_ciram(self.get_entities().custom_to_dict())