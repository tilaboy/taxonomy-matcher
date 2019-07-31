'''
Tokenizer Class
'''
import re
from .token_position import TokenWithPos


class Tokenizer():
    '''
    A basic Tokenizer class to tokenize strings and patterns

    Parameters:

        - regexp: regexp used to tokenize the string
    '''
    def __init__(self, regexp=None):
        if regexp is not None:
            self.regexp = regexp
        else:
            self.regexp = re.compile(r'\w+|[^\w\s]+')

    def tokenize(self, text):
        '''
        tokenize

        params:

            - text: string

            - pos_info: also output the position information when tokenizing
              output: tokens (with position info)
        '''
        return [match.group() for match in self.regexp.finditer(text)]

    def tokenize_with_pos_info(self, text):
        '''
        tokenize

        params:

            - text: string

        output:

            - a list of Token object
        '''
        tokens = []
        for match in self.regexp.finditer(text):
            token = TokenWithPos(match.group(), match.start(), match.end())
            tokens.append(token)
        return tokens
