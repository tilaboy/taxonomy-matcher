"""unit tests to load data from different data resource"""
from unittest import TestCase
from taxonomy_matcher.token_trie import TokenTrie
from taxonomy_matcher.tokenizer import Tokenizer
from taxonomy_matcher.token_position import TokenizedPattern, TokenizedMatch
from taxonomy_matcher.data_utils import normalize
from taxonomy_matcher.match_patterns.patterns_gz import PatternsGZ


class TokenTrieTestCases(TestCase):
    def setUp(self):
        self.gz_file = 'tests/resource/gazetteer.txt'
        self.text = 'ab Foo bar Foo foo chao foo\nBar    foo bar foo foo'
        self.tokenizer = Tokenizer()


    def test_append_list_to_local_trie(self):
        token_trie = TokenTrie(patterns=None)
        patterns = TokenizedPattern([ "a",  "b", "c", "d"])
        self.assertEqual(
            token_trie._append_token_list_to_trie(patterns),
            {'a': {'b': {'c': {'d': {'xxENDxx': None}}}}}
        )
        patterns = TokenizedPattern(["a"])
        self.assertEqual(
            token_trie._append_token_list_to_trie(patterns),
            {'a': {'xxENDxx':None}}
        )
        patterns = TokenizedPattern([])
        self.assertEqual(
            token_trie._append_token_list_to_trie(patterns),
            {'xxENDxx':None}
        )

    def test_build_from_patterns(self):
        patterns = ["foo bar",
                    "foo",
                    "foo bar foo",
                    "bar bar foo",
                    "bar foo foo"]
        tokenzied_patterns = (
            TokenizedPattern(self.tokenizer.tokenize(normalize(pattern)))
            for pattern in patterns
        )

        token_trie = TokenTrie(patterns=tokenzied_patterns)
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
        patterns = ['b tree', 'b- tree', 'B-tree']
        tokenzied_patterns = (
            TokenizedPattern(self.tokenizer.tokenize(normalize(pattern)))
            for pattern in patterns
        )
        token_trie = TokenTrie(patterns=tokenzied_patterns)
        self.assertEqual(token_trie.token_trie,
            {'b': {'-': {'tree':
                {'xxENDxx': None}},
                'tree':
                {'xxENDxx': None}}})


    def test_match_at_position(self):
        patterns = PatternsGZ(self.tokenizer, self.gz_file)
        token_trie = TokenTrie(patterns=patterns.tokenized_pattern)
        tokens = self.tokenizer.tokenize_with_pos_info(normalize(self.text))

        self.assertEqual(
            [
                [token.text for token in match.tokens]
                for match in (token_trie.match_at_position(
                                token_trie.token_trie,
                                tokens[1:])
                             )
            ],
            [['foo', 'bar'], ['foo', 'bar', 'foo']]
        )

        self.assertEqual(
            [
                [token.text for token in match.tokens]
                for match in (token_trie.match_at_position(
                                token_trie.token_trie,
                                tokens[2:])
                             )
            ],
            [['bar', 'foo', 'foo']]
        )

        self.assertEqual(
            [
                [token.text for token in match.tokens]
                for match in (token_trie.match_at_position(
                                token_trie.token_trie,
                                tokens[3:])
                             )
            ],
            []
        )


    def test_longest_match_at_position(self):
        patterns = PatternsGZ(self.tokenizer, self.gz_file)
        token_trie = TokenTrie(patterns=patterns.tokenized_pattern)

        tokens = self.tokenizer.tokenize_with_pos_info(normalize(self.text))

        self.assertEqual(
            [
                token.text
                for token in token_trie.longest_match_at_position(
                                token_trie.token_trie,
                                tokens[1:]).tokens
            ],
            ['foo', 'bar', 'foo']
        )

        self.assertEqual(
            [
                token.text
                for token in token_trie.longest_match_at_position(
                                token_trie.token_trie,
                                tokens[2:]).tokens
            ],
            ['bar', 'foo', 'foo']
        )

        self.assertEqual(
            [
                token.text
                for token in token_trie.longest_match_at_position(
                                token_trie.token_trie,
                                tokens[3:])
            ],
            []
        )
