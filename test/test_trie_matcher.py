"""unit tests to load data from different data resource"""
from unittest import TestCase
from gz_matcher.trie import TokenTrie
from gz_matcher.data_utils import tokenize

class TrieMatcherTestCases(TestCase):
    def setUp(self):
        self.gz_file = 'test/resource/gazetteer.txt'
        self.text = 'ab Foo bar Foo foo chao foo\nBar    foo bar foo foo'
        #self.gz_file = 'test/resource/compskill.txt'
        #with open('test/resource/cv1.xml') as input_fh:
        #    self.text = input_fh.read()
        self.token_trie = TokenTrie.build_from_gz(self.gz_file)

    def test_trie_match(self):
        all_matches = []
        for (match, idx) in self.token_trie.search_patterns(tokenize(self.text)):
            print(match, idx)
            all_matches.append(match)
        self.assertEqual(all_matches,
            ['foo bar',
             'foo bar foo',
             'bar foo foo',
             'chao',
             'foo bar',
             'foo bar foo',
             'foo bar',
             'foo bar foo',
             'bar foo foo'])


    def test_trie_longest_match(self):
        all_matches = []
        for match in self.token_trie.search_longest_patterns(self.text):
            print(match)
            all_matches.append(match)
        self.assertEqual(all_matches,
            [{'text': 'foo bar foo', 'start': 3, 'end': 13, 'nr_tokens': 3},
            {'text': 'chao', 'start': 19, 'end': 22, 'nr_tokens': 1},
            {'text': 'foo bar foo', 'start': 35, 'end': 45, 'nr_tokens': 3}])
