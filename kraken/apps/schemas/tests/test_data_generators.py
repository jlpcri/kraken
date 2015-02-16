from django.test import TestCase

from kraken.apps.schemas.utils import data_generators

class TestNumberGenerator(TestCase):
    def setUp(self):
        self.iterations = 20000

    def test_single_no_kwargs(self):
        for _ in range(self.iterations):
            result = data_generators.number(3, int, 1)
            self.assertIsInstance(result, list, 'test_single_no_kwargs result {0} is not a list'.format(result))
            self.assertEqual(1, len(result), 'test_single_no_kwargs len {0} of {1} too long'.format(len(result), result))
            self.assertLessEqual(len(str(result[0])), 3,
                                 'test_single_no_kwargs result {0} exceeds constraint length ({1} of 3)'.format(result[0], len(str(result[0]))))
            self.assertIsInstance(result[0], int, 'test_single_no_kwargs element {0} is not int'.format(result[0]))

    def test_list_no_kwargs(self):
        list_len = self.iterations
        result = data_generators.number(7, int, list_len)
        self.assertIsInstance(result, list, 'test_list_no_kwargs result {0} is not a list'.format(result))
        self.assertEqual(list_len, len(result), 'test_list_no_kwargs len {0} of {1} too long'.format(len(result), result))
        for i in range(list_len):
            self.assertLessEqual(len(str(result[i])), 7,
                             'test_list_no_kwargs result {0} exceeds constraint length ({1} of 7)'.format(result[i], len(str(result[i]))))
            self.assertIsInstance(result[i], int, 'test_list_no_kwargs element {0} is not int'.format(result[i]))

    def test_one_digit_max(self):
        for _ in range(self.iterations):
            list_len = 2
            result = data_generators.number(2, int, list_len, digit_max=1)
            self.assertIsInstance(result, list, 'test_one_digit_max result {0} is not a list'.format(result))
            self.assertEqual(2, len(result), 'test_one_digit_max len {0} of {1} too long'.format(len(result), result))
            for i in range(list_len):
                self.assertLessEqual(len(str(result[i])), 1,
                                     'test_one_digit_max result {0} exceeds constraint length ({1} of 1)'.format(result[i], len(str(result[i]))))
                self.assertIsInstance(result[i], int, 'test_one_digit_max element {0} is not int'.format(result[i]))

    def test_two_digit_min(self):
        for _ in range(self.iterations):
            list_len = 2
            result = data_generators.number(2, int, list_len, digit_min=2)
            self.assertIsInstance(result, list, 'test_two_digit_min result {0} is not a list'.format(result))
            self.assertEqual(2, len(result), 'test_two_digit_min len {0} of {1} too long'.format(len(result), result))
            self.assertLessEqual(result[0], 99, 'test_two_digit_min element {0} too large'.format(result[0]))
            self.assertLessEqual(result[1], 99, 'test_two_digit_min element {0} too large'.format(result[1]))
            self.assertGreaterEqual(result[0], 10, 'test_two_digit_min element {0} too small'.format(result[0]))
            self.assertGreaterEqual(result[1], 10, 'test_two_digit_min element {0} too small'.format(result[1]))