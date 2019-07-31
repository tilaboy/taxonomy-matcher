'''
Token Classes:

various class to help store tokens with extra informations
    - TokenWithPos
    - TokenizedPattern
    - TokenizedMatch
'''


class TokenWithPos:
    '''
    TokenWithPos: token with start and end position in the text
        attributes:
        - text: text in the normalized form
        - start_pos: start position
        - end_pos: end position
    '''
    def __init__(self, text, start_pos, end_pos):
        self.text = text
        self.start_pos = start_pos
        self.end_pos = end_pos

    def __repr__(self):
        return "{} [{}:{}]".format(self.text, self.start_pos, self.end_pos)


class TokenizedPattern:
    '''
    TokenizedPattern: tokenized patterns with codeid
        attributes:
        - tokens: tokens from the pattern
        - code_id: the codeid of this pattern belong to
        - skill_likelihood: the likelihood of this pattern to be a skill
    '''
    def __init__(self, tokens, code_id=None, skill_likelihood=None):
        self.tokens = tokens
        self.code_id = code_id
        self.skill_likelihood = skill_likelihood

    def __repr__(self):
        return "\ntokens: {}\ncode id: {}\nskill_likelihood: {}]".format(
            self.tokens, self.code_id, self.skill_likelihood)

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
        return [self.tokens[0].start_pos, self.tokens[-1].end_pos]

    def __repr__(self):
        return "\ntokens: {}\ncode id: {}\nstart: {}\nend: {}]".format(
            self.tokens,
            self.code_id,
            self.tokens[0].start_pos,
            self.tokens[-1].end_pos)
