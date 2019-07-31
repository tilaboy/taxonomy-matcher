'''
TokenTrie:

Token based trie strcture. The trie is build from a sequence of tokens, and
each token may has the position information from the origin text.

'''

import json
from .token_position import TokenizedMatch


class TokenTrie():
    '''
    A basic trie class for token, used for quick token sequence searching

    Paramters:
        - patterns: a list of tokenized pattern object
        - end_token: a special string to mark the end of a pattern sequence
    '''
    def __init__(self, patterns=None):
        self.token_trie = dict()
        self.end_token = 'xxENDxx'
        if patterns:
            self._build(patterns)

    def __repr__(self):
        return json.dumps(self.token_trie, indent=4)

    def _build(self, patterns):
        for pattern in patterns:
            self._add_tokens_to_trie(self.token_trie, pattern)
        return

    def _add_tokens_to_trie(self, sub_trie, pattern):
        token = pattern.tokens.pop(0)
        if token in sub_trie:
            if pattern.tokens:
                self._add_tokens_to_trie(sub_trie[token], pattern)
            else:
                sub_trie[token][self.end_token] = pattern.code_id
        else:
            local_trie = self._append_token_list_to_trie(pattern)
            sub_trie[token] = local_trie
        return

    def _append_token_list_to_trie(self, pattern):
        local_trie = {self.end_token: pattern.code_id}
        for index in range(len(pattern.tokens) - 1, -1, -1):
            local_trie = {pattern.tokens[index]: local_trie}
        return local_trie

    def match_at_position(self, sub_trie, tokens):
        '''
        search all matched phrases start at fixed position

        params:
            - sub_trie: token_trie or part of the token_trie
            - tokens: tokens from the input text,

        output:
            - all matched sequences
        '''
        matched = []
        for token in tokens:
            if token.text in sub_trie:
                sub_trie = sub_trie[token.text]
                matched.append(token)
                if self.end_token in sub_trie:
                    yield TokenizedMatch(
                        matched[:],
                        sub_trie[self.end_token],
                    )
            else:
                break

    def longest_match_at_position(self, sub_trie, tokens):
        '''
        get the last(natually to be the longest) matched phrases start at any
        fixed position

        params:
            - sub_trie: token_trie or part of the token_trie
            - tokens: tokens from the input text,

        output:
            - all matched sequences
        '''
        last_match = []
        all_matches = list(self.match_at_position(sub_trie, tokens))
        if all_matches:
            last_match = all_matches[-1]
        return last_match
