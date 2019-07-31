"""unit tests to load data from different data resource"""
import json
from unittest import TestCase
from taxonomy_matcher.matcher import Matcher

class TrieMatcherTestCases(TestCase):
    def setUp(self):
        self.ct_file = 'tests/resource/test_codetable.xml'

    def test_build_from_ct(self):
        ct_matcher = Matcher(codetable=self.ct_file)
        self.assertEqual(ct_matcher.trie_matcher.token_trie,
        {
            "female": {"xxENDxx": "2",
            "or": {"vrouw": {"xxENDxx": "2"}},
            "/": {"femme": {"xxENDxx": "2"}}},
            "male": {"xxENDxx": "1",
            "or": {"man": {"xxENDxx": "1"}},
            "/": {"homm": {"xxENDxx":"1"}}},
            "transgender": {"xxENDxx": "3"},
            "before": {"male": {"now": {"female": {"xxENDxx": "3"}}},
            "female": {"now": {"male": {"xxENDxx": "3"}}}}
        })


    def test_ct_trie_match(self):
        ct_matcher = Matcher(codetable=self.ct_file)
        text = 'ab female bar male/homm foo before female\n     now male foo'

        self.assertEqual(
            [
                (
                    match.surface_form,
                    match.start_pos,
                    match.end_pos,
                    match.code_description
                )
                for match in list(ct_matcher.matching(text))
            ],
            [
                ('female', 3, 8, 'Female'),
                ('male/homm', 14, 22, 'Male'),
                ('before female\n     now male', 28, 54, 'Transgender')
            ]
        )

        text = 'female ab Foo male or man foo before male now female'
        self.assertEqual(
            [
                (
                    match.surface_form,
                    match.start_pos,
                    match.end_pos,
                    match.code_id
                )
                for match in list(ct_matcher.matching(text))
            ],
            [
                ('female', 0, 5, '2'),
                ('male or man', 14, 24, '1'),
                ('before male now female', 30, 51, '3')
            ]
        )
