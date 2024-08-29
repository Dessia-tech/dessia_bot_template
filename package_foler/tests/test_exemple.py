import unittest

import numpy as npy


class TestClassName(unittest.TestCase):
    def test_method_name(self):
        results = [0, 3, 0]
        self.assertTrue(npy.all(results == npy.array([0, 3, 0])))


if __name__ == "__main__":
    unittest.main()
