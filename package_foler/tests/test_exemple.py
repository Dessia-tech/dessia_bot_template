import unittest
import numpy as np


class TestClassName(unittest.TestCase):

    def test_method_name(self):
        results = [0, 3, 0]
        self.assertTrue(np.all(results == np.array([0, 3, 0])))


if __name__ == "__main__":
    unittest.main()
