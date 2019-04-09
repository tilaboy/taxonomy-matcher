"""unit tests to load data from different data resource"""
import pprint
import json
from unittest import TestCase
from gz_matcher.token_trie import TokenTrie


class TokenTrieTestCases(TestCase):
    def setUp(self):
        self.gz_file = 'test/resource/gazetteer.txt'
        self.text = 'ab Foo bar Foo foo chao foo\nBar    foo bar foo foo'


    def test_append_list_to_local_trie(self):
        token_trie = TokenTrie()
        token_list = [ "a",  "b", "c", "d"]
        self.assertEqual(
            token_trie._append_token_list_to_trie([ "a",  "b", "c", "d"]),
            {'a': {'b': {'c': {'d': {'xxENDxx': None}}}}}
        )
        self.assertEqual(
            token_trie._append_token_list_to_trie([ "a" ]),
            {'a': {'xxENDxx':None}}
        )
        self.assertEqual(
            token_trie._append_token_list_to_trie([]),
            {'xxENDxx':None}
        )

    def test_build_from_patterns(self):
        patterns = [ ["foo",  "bar"],
                    ["foo"],
                    ["foo", "bar", "foo"],
                    ["bar", "bar", "foo"],
                    ["bar", "foo", "foo"]
        ]
        token_trie = TokenTrie(patterns=patterns)
        self.assertEqual(token_trie.token_trie,
            {'bar':
                {'bar':
                    {'foo':
                        {'xxENDxx': None}
                    },
                 'foo':
                    {'foo':
                        {'xxENDxx': None}
                    }
                 },
             'foo':
                {'bar':
                    {'foo':
                        {'xxENDxx': None},
                     'xxENDxx': None},
                 'xxENDxx': None}
            })

    def test_build_from_repeated_pattern(self):
        patterns = [['b', 'tree'], ['b', '-', 'tree'], ['b', '-', 'tree']]
        token_trie = TokenTrie(patterns=patterns)
        self.assertEqual(token_trie.token_trie,
            {'b': {'-': {'tree': {'xxENDxx': None}}, 'tree': {'xxENDxx': None}}})


    def test_build_from_gz(self):
        token_trie = TokenTrie.build_from_gz(self.gz_file)
        self.assertEqual(token_trie.token_trie,
            {
            'abc': {'def': {'fed': {'xxENDxx': None}}},
            'bar': {'foo': {'foo': {'xxENDxx': None}}},
            'chao': {'xxENDxx': None},
            'foo': {'bar': {'foo': {'xxENDxx': None}, 'xxENDxx': None}},
            'new': {'foo': {'xxENDxx': None}},
            'old': {'foo': {'xxENDxx': None}}})
