from dataclasses import dataclass
from typing import List

@dataclass
class Vector3:
    x: float
    y: float
    z: float


@dataclass
class Quaternion:
    x: float
    y: float
    z: float
    w: float


@dataclass
class TransformData:
    position: Vector3
    rotation: Quaternion
    scale: Vector3


@dataclass
class TrackableID:
    internal: int

    def __repr__(self):
        return f"TrackableID({self.internal})"


@dataclass
class RecordingTrackerData:
    id: TrackableID
    transform: TransformData


@dataclass
class FrameRate:
    numerator: int
    denominator: int

    def as_double(self):
        return self.numerator / self.denominator

    def frame_duration(self):
        return self.denominator / self.numerator


@dataclass
class RecordingMetadata:
    sceneName: str
    fps: FrameRate


@dataclass
class RecordingFrameData:
    frame: int
    timeCode: float
    trackers: List[RecordingTrackerData]


@dataclass
class RecordingData:
    version: int
    metadata: RecordingMetadata
    frames: List[RecordingFrameData]

    @classmethod
    def from_dict(cls, data: dict) -> 'RecordingData':
        return cls(
            version=data["version"],
            metadata=RecordingMetadata(
                sceneName=data["metadata"]["sceneName"],
                fps=FrameRate(**data["metadata"]["fps"]),
            ),
            frames=[
                RecordingFrameData(
                    frame=frame["frame"],
                    timeCode=frame["timeCode"],
                    trackers=[
                        RecordingTrackerData(
                            id=TrackableID(**tracker["id"]),
                            transform=TransformData(
                                position=Vector3(**tracker["transform"]["position"]),
                                rotation=Quaternion(**tracker["transform"]["rotation"]),
                                scale=Vector3(**tracker["transform"]["scale"]),
                            ),
                        )
                        for tracker in frame["trackers"]
                    ],
                )
                for frame in data["frames"]
            ],
        )
