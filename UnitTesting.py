import unittest
from Jsontest import convert_json_1, convert_json_2


class TestFileName(unittest.TestCase):
    def test_json_convertion(self):
        one = convert_json_1()
        two = convert_json_2()
        self.assertTrue(len(one) > 0)
        self.assertTrue(len(two) > 0)


if __name__ == '__main__':
    unittest.main()