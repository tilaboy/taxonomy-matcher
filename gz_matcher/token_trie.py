from gz_matcher.tokenizer import Tokenizer

class TokenTrie():

    def __init__(self, patterns=None, tokenizer=None):
        self.token_trie = dict()
        self.end_token = 'xxENDxx'
        self.tokenizer = tokenizer or Tokenizer()
        if patterns:
            self._build(patterns)


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
