"""unit tests to load data from different data resource"""
from unittest import TestCase
from taxonomy_matcher.matcher import Matcher

class TrieMatcherTestCases(TestCase):
    def setUp(self):
        self.gz_file = 'tests/resource/gazetteer.txt'

    def test_build_from_gz(self):
        taxonomy_matcher = Matcher(gazetteer=self.gz_file)
        self.assertEqual(taxonomy_matcher.trie_matcher.token_trie,
            {
            'abc': {'def': {'fed': {'xxENDxx': ('abc def fed', None)}}},
            'foo': {'bar': {'xxENDxx': ('foo bar', None),
            'foo': {'xxENDxx': ('foo bar foo', None)}}},
            'old': {'foo': {'xxENDxx': ('old foo', None)}},
            'new': {'foo': {'xxENDxx': ('new  foo', None)}},
            'bar': {'foo': {'foo': {'xxENDxx': ('bar foo foo', None)}}},
            'chao': {'xxENDxx': ('chao', None)}}
        )

    def test_gz_trie_match(self):
        taxonomy_matcher = Matcher(gazetteer=self.gz_file)
        text = 'ab Foo bar Foo foo chao foo\nBar    foo bar foo foo'

        self.assertEqual(
            [
                (match.surface_form, match.start_pos, match.end_pos)
                for match in list(taxonomy_matcher.matching(text))
            ],
            [
                ('Foo bar Foo', 3, 13),
                ('chao', 19, 22),
                ('foo\nBar    foo', 24, 37),
                ('bar foo foo', 39, 49)
            ]
        )

        text = 'ab Foo Foo foo foo\nBar     bar foo foo'
        self.assertEqual(
            [
                (match.surface_form, match.start_pos, match.end_pos)
                for match in list(taxonomy_matcher.matching(text))
            ],
            [
                ('foo\nBar', 15, 21),
                ('bar foo foo', 27, 37)
            ]
        )
