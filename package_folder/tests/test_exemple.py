import unittest


class TestClassName(unittest.TestCase):
    def test_method_name(self) -> None:
        results = [0, 3, 0]
        self.assertEqual([0, 3, 0], results)


if __name__ == "__main__":
    unittest.main()
