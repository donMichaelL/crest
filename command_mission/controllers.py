import json

from services.geo_services import publish_to_geo_areas
from services.redis_services import write_data_to_redis
from services.models import HandleKafkaTopic

from .models import AreaEntity, CameraEntity


class TOP21_01_COMMAND_CENTER_MISSION(HandleKafkaTopic):
    def _store_areas(self, data_dict):
        areas = AreaEntity.schema().load(data_dict["body"]["mission"]["areas"], many=True)
        write_data_to_redis("areas", AreaEntity.schema().dumps(areas, many=True))
    
    def _store_cameras(self, data_dict):
        cameras= CameraEntity.schema().load(
                data_dict["body"]["mission"]["equipment"]["cameras"], many=True
        )
        [write_data_to_redis(camera.deviceId, camera.to_json()) 
            for camera in cameras if (camera.areaInOut and camera.area)]

    def execute(self):
        super().execute()
        data_dict = json.loads(self.msg)
        self._store_areas(data_dict)
        self._store_cameras(data_dict)
        publish_to_geo_areas(self.msg)