import unittest

from event_horizon_py import FrameRate, Quaternion, RecordingData, TrackableID, Vector3


class RecordingDataTestCase(unittest.TestCase):
    def test_from_dict(self):
        # Test case 1: Valid data
        data = {
            "version": 1,
            "metadata": {
                "sceneName": "Test Scene",
                "fps": {"numerator": 30, "denominator": 1},
            },
            "frames": [
                {
                    "frame": 1,
                    "timeCode": 0,
                    "trackers": [
                        {
                            "id": {"internal": 1},
                            "transform": {
                                "position": {"x": 0, "y": 0, "z": 0},
                                "rotation": {"x": 0, "y": 0, "z": 0, "w": 1},
                                "scale": {"x": 1, "y": 1, "z": 1},
                            },
                        }
                    ],
                }
            ],
        }
        recording_data = RecordingData.from_dict(data)
        self.assertEqual(recording_data.version, 1)
        self.assertEqual(recording_data.metadata.sceneName, "Test Scene")
        self.assertEqual(recording_data.metadata.fps, FrameRate(30, 1))
        self.assertEqual(len(recording_data.frames), 1)
        self.assertEqual(recording_data.frames[0].frame, 1)
        self.assertEqual(recording_data.frames[0].timeCode, 0)
        self.assertEqual(len(recording_data.frames[0].trackers), 1)
        self.assertEqual(recording_data.frames[0].trackers[0].id, TrackableID(1))
        self.assertEqual(
            recording_data.frames[0].trackers[0].transform.position, Vector3(0, 0, 0)
        )
        self.assertEqual(
            recording_data.frames[0].trackers[0].transform.rotation,
            Quaternion(0, 0, 0, 1),
        )
        self.assertEqual(
            recording_data.frames[0].trackers[0].transform.scale, Vector3(1, 1, 1)
        )


class FrameRateTestCase(unittest.TestCase):
    def test_as_double(self):
        # Test case 1: Positive numerator and denominator
        framerate = FrameRate(30, 1)
        self.assertEqual(framerate.as_double(), 30.0)

        # Test case 2: Negative numerator and positive denominator
        framerate = FrameRate(-24, 1)
        self.assertEqual(framerate.as_double(), -24.0)

    def test_frame_duration(self):
        # Test case 1: Positive numerator and denominator
        framerate = FrameRate(30, 1)
        self.assertEqual(framerate.frame_duration(), 1 / 30)

        # Test case 2: Negative numerator and positive denominator
        framerate = FrameRate(-24, 1)
        self.assertEqual(framerate.frame_duration(), 1 / -24)
