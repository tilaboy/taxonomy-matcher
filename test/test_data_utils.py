"""unit tests to load data from different data resource"""
from unittest import TestCase
from gz_matcher.data_utils import prepare_from_gz

class DataUtilsTestCases(TestCase):
    def setUp(self):
        pass

    def test_prepare_from_gz(self, gz_file='test/resource/gazetteer.txt'):
        patterns = prepare_from_gz(gz_file)
        print(patterns)
        self.assertEqual(patterns,
            [['abc', 'def', 'fed'],
             ['foo', 'bar'],
             ['old', 'foo'],
             ['new', 'foo'],
             ['foo', 'bar', 'foo'],
             ['bar', 'foo', 'foo'],
             ['chao']])
