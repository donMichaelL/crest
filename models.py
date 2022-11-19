import requests

from settings import NATIONAL_DB_URL, SUSPECT_ATTRS_SET, VEHICLE_ATTRS_SET, CIRCLING_THRESHOLD, CIRCLING_THRESHOLD_NUMBER
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, Undefined, config
from typing import List, Optional, Set
from time import time

from utils import check_server_for_restricted_area


@dataclass
class ConvoyItem:
    license_plates: Optional[Set[str]] = field(default_factory=set)
    timestamp_in_min: Optional[int] = 0


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class CameraEntity:
    deviceId: str
    areaInOut: str = ""

    def is_cameraIn(self):
        return self.areaInOut == 'In'


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class CirclingPlatesEntity:
    plate: Optional[str]
    timestamps_in_min: Optional[List[int]] = field(default_factory=list)


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class AreaEntity:
    name: str
    vehiclesIn: Optional[int] = 0
    vehiclesOut: Optional[int] = 0
    vehicleCount: Optional[int] = 0
    licensePlates: Optional[List[str]] = field(default_factory=list)
    circlingPlates: Optional[List[CirclingPlatesEntity]] = field(default_factory=list, metadata=config(exclude=lambda x:True))
    circlingPlatesReport: Optional[List[str]] = field(default_factory=list)

    def add_vehicle(self, plate):        
        self.vehiclesIn +=1
        self.vehicleCount += 1
        self.licensePlates.append(plate)

    def add_circling_vehicle(self, plate):    
        found = False
        for circling_plate in self.circlingPlates:
            if circling_plate.plate == plate:
                circling_plate.timestamps_in_min.append(int(time()) // 60)
                found = True
        if not found:
            self.circlingPlates.append(CirclingPlatesEntity(plate, [int(time()) // 60]))

    def _check_vehicle_circling(self, licence_plate: str):
        current_timestamp_in_min = int(time()) // 60
        for circling_plate in self.circlingPlates:
            if circling_plate.plate == licence_plate:
                for timestamp in circling_plate.timestamps_in_min[:]:
                    if current_timestamp_in_min - timestamp > CIRCLING_THRESHOLD:
                        circling_plate.timestamps_in_min.remove(timestamp)
            if len(circling_plate.timestamps_in_min) > CIRCLING_THRESHOLD_NUMBER:
                self.circlingPlatesReport.append(licence_plate)
            elif licence_plate in self.circlingPlatesReport:
                self.circlingPlatesReport.remove(licence_plate)
            return self.circlingPlatesReport

    def remove_vehicle(self, plate):
        self.vehiclesOut +=1
        self.vehicleCount -= 1
        self.licensePlates.remove(plate)


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class PlateDetectedEntity:
    text: str
    score: float
    url: str
    car_id: int
    timestamp: str
    country: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class DetectionEntity:
    deviceID: str
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
            print(str(err))

    def __post_init__(self):
        self.severity, self.description, self.area = check_server_for_restricted_area(self.detection.deviceID)
        self.get_info_from_db()

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
                    "deviceID": self.body.deviceId,
                    "platesDetected": {
                        "text": value.replace(' ', '%20'),
                        "score": self.body.platesDetected.scores[index],
                        "url": (self.body.platesDetected.url[index: ]+[''])[0],
                        "car_id": (self.body.platesDetected.car_id[index: ]+[''])[0],
                        "timestamp": (self.body.platesDetected.timestamp[index: ]+[''])[0],
                        "country": (self.body.platesDetected.country[index: ]+[''])[0],
                    }
                }
            }) for index, value in enumerate(self.body.platesDetected.text)  if self.body.platesDetected.scores[index] >= 0.7
        ]
    
    def custom_to_dict(self):
        result = self.to_dict()
        result['LPR']['case_id'] = self.header.caseId
        result['LPR']['platesDetected'] = result.pop('plates_detected')
        return result
        

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class ObjectDetectionBodyEntity:
    deviceId: str
    mediaRootId: str
    domainId: str
    objectsDetected: dict


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class ObjectDetectionEntity:
    header: Header = field(metadata=config(exclude=lambda x:True))
    body: ObjectDetectionBodyEntity = field(metadata=config(field_name="objectsDet"))

    def custom_to_dict(self):
        result = self.to_dict()
        result['objectsDet']['caseID'] = self.header.caseId
        return result

