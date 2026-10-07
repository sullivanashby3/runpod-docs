import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).parents[1]))
from cost.calculator import compare


class CostTests(unittest.TestCase):
    def test_units_and_runtime(self):
        result = compare(3, 60, .1, 60)
        self.assertEqual(result["gpu_estimate"], .00083333)
        self.assertEqual(result["runtime_seconds"], 1.0)

    def test_startup_storage_and_utilization_are_visible(self):
        result = compare(3, 10, .1, 60, startup_seconds=20, utilization=.5, storage_hourly=1)
        self.assertGreater(result["gpu_estimate"], 0)
        self.assertEqual(result["assumptions"]["utilization"], .5)
        self.assertEqual(result["assumptions"]["startup_seconds"], 20)

    def test_bad_inputs_fail(self):
        with self.assertRaises(ValueError):
            compare(3, 0, .1, 60)
        with self.assertRaises(ValueError):
            compare(3, 10, .1, 60, utilization=1.1)


if __name__ == "__main__":
    unittest.main()
