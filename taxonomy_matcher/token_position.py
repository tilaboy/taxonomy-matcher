'''
Token Classes:

various class to help store tokens with extra informations
    - TokenizedPattern
    - TokenizedMatch
'''


class TokenizedPattern:
    '''
    TokenizedPattern: tokenized patterns with codeid
        attributes:
        - tokens: tokens from the pattern
        - code_id: the codeid of this pattern belong to
        - skill_likelihood: the likelihood of this pattern to be a skill
    '''
    def __init__(self, tokens, surface_form='', code_id=None):
        self.tokens = tokens
        self.surface_form = surface_form
        self.code_id = code_id

    def __repr__(self):
        return "\ntokens: {}\ncode id: {}]".format(self.tokens, self.code_id)

    def pattern_form(self):
        return " ".join([token.text for token in self.tokens])


class TokenizedMatch(TokenizedPattern):
    '''
    TokenizedMatch: tokenized patterns with codeid
        attributes:
        - tokens: tokens from the pattern
        - code_id: the codeid of this pattern belong to

        difference with TokenizedPattern:
        - each token in TokenizedMatch.tokens is a instance of TokenWithPos
        - token in TokenziedPattern.token is simply the token list without
        position
    '''

    def text_range(self):
        return [self.tokens[0].start, self.tokens[-1].end]

    def __repr__(self):
        return "\ntokens: {}\ncode id: {}\nstart: {}\nend: {}]".format(
            self.tokens,
            self.code_id,
            self.tokens[0].start,
            self.tokens[-1].end)
