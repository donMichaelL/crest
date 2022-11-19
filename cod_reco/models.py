from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, Undefined, config
from typing import List


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Header:
    caseId: str
    sender: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class CODDetectionBodyEntity:
    deviceID: str = field(metadata=config(field_name="device-ID"))
    imageURL: str
    concealedObjects: List


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class CODDetectionEntity:
    header: Header = field(metadata=config(exclude=lambda x:True))
    body: CODDetectionBodyEntity = field(metadata=config(field_name="concealedObjectsDet"))
    
    def custom_to_dict(self):
        result = self.to_dict()
        result['concealedObjectsDet']['caseID'] = self.header.caseId
        return result