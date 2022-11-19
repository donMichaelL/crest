from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, Undefined, config


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Header:
    caseId: str
    sender: str

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
