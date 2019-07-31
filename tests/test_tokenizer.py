# -*coding: utf-8 -*-
from unittest import TestCase
from taxonomy_matcher.tokenizer import Tokenizer
from taxonomy_matcher.matcher import Matcher

class TokenizerTestCases(TestCase):
    def setUp(self):
        self.tokenizer = Tokenizer()

    def test_simple_sentence(self):
        text = 'this is a normal sentence'
        self.assertEqual(
            self.tokenizer.tokenize(text),
            ['this', 'is', 'a', 'normal', 'sentence']
        )

        text = 'this is a normal-sentence'
        self.assertEqual(
            self.tokenizer.tokenize(text),
            ['this', 'is', 'a', 'normal', '-', 'sentence']
        )

        text = 'this is a normal_sentence'
        self.assertEqual(
            self.tokenizer.tokenize(text),
            ['this', 'is', 'a', 'normal_sentence']
        )


    def test_char_with_hat(self):
        text = 'Alp NADİ\nCoordination potential bidders.'
        self.assertEqual(
            self.tokenizer.tokenize(text),
            ['Alp', 'NADİ', 'Coordination', 'potential', 'bidders', '.']
        )
        text = 'Hurmoğlu, Botaş BTC, 2002\nCoordination of packages.'
        self.assertEqual(
            self.tokenizer.tokenize(text),
            ['Hurmoğlu',
             ',',
             'Botaş',
             'BTC',
             ',',
             '2002',
             'Coordination',
             'of',
             'packages',
             '.']
        )
