'''MatchPatters: basic modules for tokenized patterns'''
import os
from taxonomy_matcher.data_utils import normalize
from taxonomy_matcher.token_position import TokenizedPattern


class Patterns():
    '''
    Patterns:

    Basic class to store the pattern information
    '''
    def __init__(self, tokenizer, pattern_file):
        self.tokenizer = tokenizer
        if os.path.isfile(pattern_file):
            self.pattern_file = pattern_file
        else:
            raise Exception("ERROR: could not found file 'pattern_file': {}"
                            .format(pattern_file))

    def pattern_tokens_generator(self, source):
        '''
        tokenize each instance in the codetable

        params:
            - source: the source of the patterns

        output:
            - iterator of token list, e.g. (['a', 'b'], ['c', 'd', 'e'])
        '''

        for (instance, code_id) in self.pattern_instance_generator(source):
            yield TokenizedPattern(
                self.tokenizer.tokenize(normalize(instance)),
                code_id
            )

    def pattern_instance_generator(self, source):
        '''to be implemented in the sub class'''
        raise Exception("Error: instance generator is not implemented")


class PatternTypes():
    '''
    PatternTypes:

    Basic class to store the pattern file type
    '''
    PATTERN_FILE_TYPE_GZ = 'gazetteer'
    PATTERN_FILE_TYPE_CT = 'codetable'
    PATTERN_FILE_TYPE_NT = 'normalization_table'
    PATTERN_FILE_TYPE_DEFAULT = 'gazetteer'
