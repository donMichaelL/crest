from services.models import HandleKafkaTopic
from services.ciram_services import post_ciram

from .models import FaceDetectionEntity

class TOP22_05_FACE_RECO_DONE(HandleKafkaTopic):
    model = FaceDetectionEntity

    def execute(self):
        super().execute()
        post_ciram(self.get_entities().custom_to_dict())