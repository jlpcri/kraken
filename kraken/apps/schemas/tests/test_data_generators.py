from django.test import TestCase

from kraken.apps.schemas.utils import data_generators

class TestNumberGenerator(TestCase):
    def test_single_no_kwargs(self):
        result = data_generators.number(3, int, 1)
        self.assertIsInstance(result, list, 'test_single_no_kwargs result is not a list')
        self.assertEqual(1, len(result), 'test_single_no_kwargs len too long')
        self.assertLessEqual(3, len(str(result[0])), 'test_single_no_kwargs result exceeds constraint length')
        self.assertIsInstance(result[0], int, 'test_single_no_kwargs element is not int')