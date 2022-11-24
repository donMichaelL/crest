from settings import CIRCLING_THRESHOLD, CIRCLING_THRESHOLD_NUMBER
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, Undefined, config
from typing import List, Optional
from time import time


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
            if len(circling_plate.timestamps_in_min) >= CIRCLING_THRESHOLD_NUMBER:
                self.circlingPlatesReport.append(licence_plate)
            elif licence_plate in self.circlingPlatesReport:
                self.circlingPlatesReport.remove(licence_plate)
            return self.circlingPlatesReport

    def remove_vehicle(self, plate):
        self.vehiclesOut +=1
        self.vehicleCount -= 1
        self.licensePlates.remove(plate)