import unittest
from square_of_sum_package.src.square_anviks.calculator import square_of_sum


class TestSquareSum(unittest.TestCase):
    def test_square_sum_int(self):
        self.assertEqual(25, square_of_sum(2, 3))
        self.assertEqual(625, square_of_sum(17, 8))

    def test_square_sum_float(self):
        self.assertEqual(65.61, square_of_sum(2.8, 5.3))
        self.assertEqual(25_234.0373300625, square_of_sum(61.6792, 97.17305))

    def test_square_sum_int_and_float(self):
        self.assertEqual(155.201764, square_of_sum(3.458, 9))
        self.assertEqual(428_368.0508828224, square_of_sum(569, 85.49832))

    def test_square_sum_not_number(self):
        self.assertEqual(-1, square_of_sum("hello", "xD"))
        self.assertEqual(-1, square_of_sum(False, True))
        self.assertEqual(-1, square_of_sum(3, None))


if __name__ == '__main__':
    unittest.main()
