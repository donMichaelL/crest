from dataclasses_json import dataclass_json, Undefined, config
from dataclasses import dataclass, field
from typing import List


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Header:
    caseId: str
    sender: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class ActivityDetected:
    activityDuration: List[float]
    score: List[float]
    className: List[str]
    classId: List[int]
    activityDescription: List[str]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class ActivityRecoBodyEntity:
    deviceId: str
    domainId: str
    activityDetected: ActivityDetected
    timestampProcessing: str
    mediaRootId: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class ActivityRecoEntity:
     header: Header = field(metadata=config(exclude=lambda x:True))
     body: ActivityRecoBodyEntity