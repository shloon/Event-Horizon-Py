from .dataclasses import FrameRate, RecordingData, RecordingFrameData, RecordingMetadata

import brotli
import json
import os
from typing import List, Tuple, Union

PathLike = Union[str, bytes, os.PathLike]

np_dtype: List[Tuple[str, str]] = [
    ("Frame", "i4"),
    ("TrackerID", "i4"),
    ("PosX", "f4"),
    ("PosY", "f4"),
    ("PosZ", "f4"),
    ("RotX", "f4"),
    ("RotY", "f4"),
    ("RotZ", "f4"),
    ("RotW", "f4"),
    ("ScaleX", "f4"),
    ("ScaleY", "f4"),
    ("ScaleZ", "f4"),
]


class Recording:
    _raw_data: RecordingData

    def __init__(self, data: RecordingData):
        self._raw_data = data

    @classmethod
    def from_file(cls, filename: PathLike) -> "Recording":
        with open(filename, "br") as file:
            data = RecordingData.from_dict(json.loads(brotli.decompress(file.read())))

        obj = cls(data)
        return obj

    def metadata(self) -> RecordingMetadata:
        return self._raw_data.metadata

    def scene_name(self) -> str:
        return self._raw_data.metadata.sceneName

    def frame_rate(self) -> FrameRate:
        return self._raw_data.metadata.fps

    def raw_data(self) -> RecordingData:
        return self._raw_data

    def raw_frames(self) -> List[RecordingFrameData]:
        return self._raw_data.frames

    try:
        from pandas import DataFrame

        pandas_df: DataFrame

        def create_tracker_pandas_view(self) -> DataFrame:
            if hasattr(self, "pandas_df") and self.pandas_df:
                return self.pandas_df

            frame_numbers = []
            tracker_ids = []
            positions = []
            rotations = []
            scales = []

            for frame in self.raw_frames():
                for tracker in frame.trackers:
                    frame_numbers.append(frame.frame)
                    tracker_ids.append(tracker.id.internal)
                    positions.append(
                        (
                            tracker.transform.position.x,
                            tracker.transform.position.y,
                            tracker.transform.position.z,
                        )
                    )
                    rotations.append(
                        (
                            tracker.transform.rotation.x,
                            tracker.transform.rotation.y,
                            tracker.transform.rotation.z,
                            tracker.transform.rotation.w,
                        )
                    )
                    scales.append(
                        (
                            tracker.transform.scale.x,
                            tracker.transform.scale.y,
                            tracker.transform.scale.z,
                        )
                    )

            import pandas as pd

            self.pandas_df = pd.DataFrame(
                {
                    "Frame": frame_numbers,
                    "TrackerID": tracker_ids,
                    "Position": positions,
                    "Rotation": rotations,
                    "Scale": scales,
                    "FrameDuration": self.frame_rate().frame_duration(),
                }
            )
            return self.pandas_df

    except ImportError as _:
        # pandas support not available
        pass

    try:
        from numpy.typing import NDArray

        np_array: NDArray

        def create_tracker_numpy_view(self) -> NDArray:
            if hasattr(self, "np_array") and self.np_array:
                return self.np_array

            import numpy as np

            data = []

            for frame in self._raw_data.frames:
                for tracker in frame.trackers:
                    frame_data = [
                        frame.frame,
                        tracker.id.internal,
                        # position
                        tracker.transform.position.x,
                        tracker.transform.position.y,
                        tracker.transform.position.z,
                        # rotation
                        tracker.transform.rotation.x,
                        tracker.transform.rotation.y,
                        tracker.transform.rotation.z,
                        tracker.transform.rotation.w,
                        # scale
                        tracker.transform.scale.x,
                        tracker.transform.scale.y,
                        tracker.transform.scale.z,
                    ]
                    data.append(frame_data)

            self.np_array = np.array(data, dtype=np_dtype)
            return self.np_array

    except ImportError as _:
        # numpy support not available
        pass
