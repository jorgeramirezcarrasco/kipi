import unittest
from utils.labels_tagging_transformer_yolov4 import rindex


class TestUtils(unittest.TestCase):

    def test_rindex(self):
        self.assertEqual(rindex([3,1,2,3,1],3), 3, "Should be 3")
        self.assertEqual(rindex([3,1,3],3), 2, "Should be 2")


if __name__ == '__main__':
    unittest.main()
