import requests
from time import time

from datetime import datetime

from settings import NATIONAL_DB_URL, SUSPECT_ATTRS_SET, VEHICLE_ATTRS_SET, CONVOY_THRESHOLD_TIME
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, Undefined, config
from typing import List, Optional, Set

from services.geo_services import check_server_for_restricted_area


DEFAULT_SUSPECT = {
    "age": 0,
    "id": 0,
    "profession": "",
    "nickname": "",
    "firstName": "",
    "email": "",
    "lastName": "",
    "lastKnownAddress": "",
    "photo": ""
}

DEFAULT_VEHICLE = {
    "licenseState": "",
    "model": "",
    "type": "",
    "id": 0,
    "color": "",
    "vin": "",
    "manufacturer": "",
    "registeredOwner": "",
    "year": 0,
    "description": "",
    "licenseNumber": "",
    "icon": ""
  }

@dataclass
class ConvoyItem:
    license_plates: Optional[Set[str]] = field(default_factory=set)
    timestamp_in_min: Optional[int] = 0

    def add_licence_plates(self, plates_detected):
        {
            self.license_plates.add(plate.detection.platesDetected.text)
            for plate in plates_detected
        }
    
    def check_and_clear_licence_plates(self):
        current_timestamp = int(time()) // 60
        if current_timestamp - self.timestamp_in_min > CONVOY_THRESHOLD_TIME:
            self.timestamp_in_min = current_timestamp
            self.license_plates.clear()


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class PlateDetectedEntity:
    text: str
    scores: float
    url: str
    car_id: int
    timestamp: List[str]
    country: List[str]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class DetectionEntity:
    deviceId: str
    platesDetected: PlateDetectedEntity


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class LPR:
    detection: DetectionEntity
    suspect: Optional[dict] = None
    vehicle: Optional[dict] = None
    severity: Optional[str] = None
    description: Optional[str] = None
    area: Optional[str] = field(default=None, metadata=config(exclude=lambda x:True))

    def get_info_from_db(self):
        text = self.detection.platesDetected.text
        response = requests.get(NATIONAL_DB_URL + text)
        try:
            suspect_dict = response.json()[0]
            self.suspect = {
                key: suspect_dict[key]
                for key in suspect_dict.keys() & SUSPECT_ATTRS_SET
            }
   
            for vehicle in suspect_dict["vehicles"]:
                if vehicle["vehicleDetails"]["licenseNumber"] == text:
                    vehicles_dict = vehicle["vehicleDetails"]
                    self.vehicle = {
                        key: vehicles_dict[key]
                        for key in vehicles_dict.keys() & VEHICLE_ATTRS_SET
                    }                        
        except Exception as err:    
            self.suspect = DEFAULT_SUSPECT.copy()
            self.vehicle = DEFAULT_VEHICLE.copy()

    def __post_init__(self):
        self.get_info_from_db()
        self.severity, self.description, self.area = check_server_for_restricted_area(self.detection.deviceId)
        area_name = self.area if self.area else "a non restricted area"
        if self.suspect["id"] != 0:
            self.description = f"ALERT in {area_name}: The vehicle {self.detection.platesDetected.text} possibly is operated by suspect {self.suspect['lastName']}! Take immediate actions for suspect vehicle containment."
        

    def to_dict(self):
        result = super().to_dict()
        result['detection'] = {
            "deviceID": result.pop('deviceID'),
            "platesDetected": result.pop('platesDetected')
        }
        return result


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Header:
    caseId: str
    sender: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class PlatesDetectedEntity:
    text: List[str]
    boxes: List
    scores: List[float]
    url: List[str]
    car_id: List[int]
    timestamp: List[str]
    country: List[str]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class LPRMessageBodyEntity:
    deviceId: str = field(metadata=config(field_name="device_id"))
    platesDetected: PlatesDetectedEntity = field(metadata=config(exclude=lambda x:True))


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class LPRMessageEntity:
    header: Header = field(metadata=config(exclude=lambda x:True))
    body: LPRMessageBodyEntity = field(metadata=config(field_name="LPR"))
    plates_detected: Optional[List[LPR]] = None

    def __post_init__(self):
        self.plates_detected = [
            LPR.from_dict({
                "detection": {
                    "deviceId": self.body.deviceId,
                    "platesDetected": {
                        "text": value.replace(' ', '%20'),
                        "scores": self.body.platesDetected.scores[index],
                        "url": (self.body.platesDetected.url[index: ]+[''])[0],
                        "car_id": (self.body.platesDetected.car_id[index: ]+[''])[0],
                        "timestamp": [str(datetime.utcnow().isoformat())],
                        "country": [(self.body.platesDetected.country[index: ]+[''])[0]],
                    }
                }
            }) for index, value in enumerate(self.body.platesDetected.text)  if self.body.platesDetected.scores[index] >= 0.7
        ]
    
    def custom_to_dict(self):
        result = self.to_dict()
        result['LPR']['case_id'] = self.header.caseId
        result['LPR']['platesDetected'] = result.pop('plates_detected')
        return result
