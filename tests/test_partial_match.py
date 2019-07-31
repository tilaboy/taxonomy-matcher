from unittest import TestCase
import tempfile
import pathlib
from taxonomy_matcher.matcher import Matcher

class ParticalMatcherTestCases(TestCase):
    def setUp(self):
        gz_content = '''dutch
dutch (flemish)
foo bar'''
        self.gz_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        with self.gz_file as f:
            f.write(gz_content)


    def test_partial_trie_match_braket(self):
        self.matcher = Matcher(gazetteer=self.gz_file.name)
        text = "November 1954 Place of Birth : Rotterdam Holland Passport : \
  dutch (Current) Domiciled in NZ : 47 years"
        self.assertEqual(
            [
                (match.surface_form, match.start_pos, match.end_pos)
                for match in list(self.matcher.matching(text))
            ],
            [
                ('dutch', 62, 66),
            ]
        )

    def test_partial_trie_match_doc_end(self):
        self.matcher = Matcher(gazetteer=self.gz_file.name)
        text = '''

foo bar
'''
        self.assertEqual(
            [
                (match.surface_form, match.start_pos, match.end_pos)
                for match in list(self.matcher.matching(text))
            ],
            [
                ('foo bar', 2, 8),
            ]
        )

    def tearDown(self):
        path = pathlib.Path(self.gz_file.name)
        path.unlink()
