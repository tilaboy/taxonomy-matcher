import re
from gz_matcher.data_utils import normalize
from gz_matcher.tokenizer import Tokenizer

class TokenTrie():

    def __init__(self, patterns=None, keyset=None, tokenizer=None):
        self.token_trie = dict()
        self.end_token = 'xxENDxx'
        self.tokenizer = tokenizer or Tokenizer()
        if patterns:
            self._build(patterns)

    @classmethod
    def build_from_list(cls, list, regexp=None):
        tokenizer = Tokenizer(regexp)
        patterns = [
            tokenizer.tokenize(normalize(line.rstrip()), pos_info=False)
            for line in list
            if not (line.startswith('#') or re.match(r'^\W+$', line))
        ]
        return cls(patterns=patterns, tokenizer=tokenizer)

    @classmethod
    def build_from_gz(cls, gz_file, regexp=None):
        tokenizer = Tokenizer(regexp)
        with open(gz_file, 'rt') as gz_fh:
            patterns = [
                tokenizer.tokenize(normalize(line.rstrip()), pos_info=False)
                for line in gz_fh
                if not (line.startswith('#') or re.match(r'^\W+$', line))
            ]
        return cls(patterns=patterns, tokenizer=tokenizer)


    def _build(self, patterns):
        for pattern in patterns:
            self._add_tokens_to_trie(self.token_trie, pattern)
        return

    def _add_tokens_to_trie(self, sub_trie, tokens):
        token = tokens.pop(0)
        if token in sub_trie:
            if tokens:
                self._add_tokens_to_trie(sub_trie[token], tokens)
            else:
                sub_trie[token][self.end_token] = None
        else:
            local_trie = self._append_token_list_to_trie(tokens)
            sub_trie[token] = local_trie
        return

    def _append_token_list_to_trie(self, tokens):
        local_trie = {self.end_token: None}
        for index in range(len(tokens) - 1, -1, -1):
            local_trie = {tokens[index]:local_trie}
        return local_trie

    def _search_at_position(self, sub_trie, tokens):
        matched = []
        for token in tokens:
            if token[0] in sub_trie:
                sub_trie = sub_trie[token[0]]
                matched.append(token)
                if self.end_token in sub_trie:
                    yield matched
            else:
                matched = []
                break


    def search_matches(self, text):
        tokens = self.tokenizer.tokenize(normalize(text))
        nr_tokens = len(tokens)
        idx = 0
        while idx < len(tokens):
            longest_matched = []
            end_of_longest_matched = 0
            for matched in self._search_at_position(self.token_trie, tokens[idx:]):
                if matched[-1][2] > end_of_longest_matched :
                    end_of_longest_matched = matched[-1][2]
                    longest_matched = matched
            if longest_matched:
                matched_string = ' '.join([word[0] for word in longest_matched])
                start = longest_matched[0][1]
                end = longest_matched[-1][2]
                yield (matched_string, start, end)
                idx += len(longest_matched)
            else:
                idx += 1
