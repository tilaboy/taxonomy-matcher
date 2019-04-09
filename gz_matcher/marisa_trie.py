from marisa_trie import Trie
from gz_matcher.data_utils import prepare_from_gz, count_tokens, tokenize
import re

class TokenTrie(Trie):
    def __init__(self, patterns=None, keyset=None, splitter=' '):
        super(TokenTrie, self).__init__(patterns)
        self.splitter = splitter

    @classmethod
    def build_from_list(cls, patterns):
        return cls(patterns=patterns)

    @classmethod
    def build_from_gz(cls, gz_file):
        patterns = prepare_from_gz(gz_file)

        return cls(patterns=[" ".join(pattern) for pattern in patterns])

    def lookup(self, query, tokens):
        if query in self:
            yield query

        if len(tokens):
            next_query = query + " " + tokens[0][0]
            if self.iterkeys(next_query):
                for ptn in self.lookup(next_query, tokens[1:]):
                    yield ptn

    def search_patterns(self, words):
        for idx, word in enumerate(words):
            for pattern in self.lookup(word[0], words[idx + 1:]):
                yield pattern, idx

    def search_longest_patterns(self, text):
        current_idx = -1000000
        match_at_pos = {}
        words = tokenize(text, pos_info=True)

        for (pattern, idx) in self.search_patterns(words):
            # update the patter if the new pattern is longer
            update_longest_pattern = 0
            nr_tokens = count_tokens(pattern)
            if current_idx == idx:
                if nr_tokens > match_at_pos[idx]['nr_tokens']:
                    update_longest_pattern = 1
            else:
                if idx > current_idx + nr_tokens - 1:
                    current_idx = idx
                    update_longest_pattern = 1
            if update_longest_pattern == 1:
                match_at_pos[idx] = {
                    'text':pattern,
                    'start': words[current_idx][1],
                    'end': words[current_idx + nr_tokens -1][2],
                    'nr_tokens': nr_tokens
                }
        for idx, match in match_at_pos.items():
            yield match
