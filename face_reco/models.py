from dataclasses_json import dataclass_json, Undefined, config
from dataclasses import dataclass, field


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Header:
    caseId: str
    sender: str

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class FaceDetectionBodyEntity:
    camID: str
    sourceURL: str
    faceRecognized: dict = field(metadata=config(field_name="face"))


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class FaceDetectionEntity:
    header: Header = field(metadata=config(exclude=lambda x:True))
    body: FaceDetectionBodyEntity = field(metadata=config(field_name="faceDet"))

    def custom_to_dict(self):
        result = self.to_dict()
        result['faceDet']['caseID'] = self.header.caseId
        return result
