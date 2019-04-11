import re

from gz_matcher.token_trie import TokenTrie
from gz_matcher.tokenizer import Tokenizer
from gz_matcher.data_utils import normalize, validate_pattern, from_file_to_list

class GazetteerMatcher():
    def __init__(
            self,
            gazetteer=None,
            codetable=None,
            blacklist=None,
            regexp=None
        ):
        self.regexp = regexp
        self.tokenizer = Tokenizer(self.regexp)
        self.blacklist = []

        if gazetteer:
            pattern_generator = self._generator_from_gz(gazetteer)
        if codetable:
            pattern_generator = self._generator_from_codetable(codetable)
        if blacklist:
            self.blacklist = from_file_to_list(blacklist)

        self.trie_matcher = TokenTrie(
            patterns=pattern_generator,
            tokenizer = self.tokenizer
            )


    def _generator_from_list(self, list ):

        return (
            self.tokenizer.tokenize(normalize(line.rstrip()), pos_info=False)
            for line in list
            if validate_pattern(line, self.blacklist)
        )


    def _generator_from_gz(self, gz_file, regexp=None):
        tokenizer = Tokenizer(regexp)
        with open(gz_file, 'rt') as gz_fh:
            for line in gz_fh:
                line = line.rstrip()
                if validate_pattern(line, self.blacklist):
                    yield self.tokenizer.tokenize(normalize(line), pos_info=False)


    # dummy function, need to be updated
    def _generator_from_codetable(self, gz_file, regexp=None):
        tokenizer = Tokenizer(regexp)
        with open(gz_file, 'rt') as gz_fh:
            patterns = gz_fh.read()
        return self._generator_from_list("\n".split(patterns))


    def matching(self, text):
        tokens = self.tokenizer.tokenize(normalize(text))
        nr_tokens = len(tokens)
        idx = 0
        while idx < len(tokens):
            longest_matched = []
            end_of_longest_matched = 0
            for matched in self.trie_matcher._search_at_position(self.trie_matcher.token_trie,tokens[idx:]):
                if matched[-1][2] > end_of_longest_matched :
                    end_of_longest_matched = matched[-1][2]
                    longest_matched = matched
            if longest_matched:
                #matched_string = ' '.join([word[0] for word in longest_matched])
                start = longest_matched[0][1]
                end = longest_matched[-1][2]
                yield (text[start:end+1], start, end)
                idx += len(longest_matched)
            else:
                idx += 1
