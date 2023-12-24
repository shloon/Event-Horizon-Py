import unittest
import os
from event_horizon_py import Recording, RecordingData
import json
import brotli


class TestRecording(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(script_dir, "data", "sample_recording.evh")

        cls.sample_file = file_path

        with open(cls.sample_file, "br") as file:
            cls.sample_data = RecordingData.from_dict(
                json.loads(brotli.decompress(file.read()))
            )

    def test_from_file(self):
        recording = Recording.from_file(self.sample_file)
        self.assertIsInstance(recording, Recording)
        self.assertIsNotNone(recording.raw_data())

    def test_metadata_access(self):
        recording = Recording(self.sample_data)
        self.assertIsNotNone(recording.metadata())
        self.assertIsInstance(recording.scene_name(), str)
        self.assertIsNotNone(recording.frame_rate())

    def test_create_tracker_pandas_view(self):
        recording = Recording(self.sample_data)
        df = recording.create_tracker_pandas_view()
        self.assertIsNotNone(df)
        self.assertEqual(df.shape[1], 6)

    def test_create_tracker_numpy_view(self):
        recording = Recording(self.sample_data)
        np_array = recording.create_tracker_numpy_view()
        self.assertIsNotNone(np_array)
        self.assertEqual(np_array.ndim, 2)


if __name__ == "__main__":
    unittest.main()
