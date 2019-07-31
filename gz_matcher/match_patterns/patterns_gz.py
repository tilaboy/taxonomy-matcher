'''MatchPatters: module to load GZ/CT/NT to the tokenized patterns'''
from taxonomy_matcher.data_utils import has_content
from .patterns import Patterns
from .patterns import PatternTypes


class PatternsGZ(Patterns):
    '''
    PatternsGZ:

    Class to store pattern information from Gazetteer file

    attibutes:

    - codeid_description: empty dictionary

    - tokenized_pattern: a tokenized pattern generator
    '''

    def __init__(self, tokenizer, pattern_file):
        super(PatternsGZ, self).__init__(tokenizer, pattern_file)
        self.pattern_file_type = PatternTypes.PATTERN_FILE_TYPE_GZ
        self.codeid_description = self.codeid_description_mapping()
        self.tokenized_pattern = self.pattern_tokens_generator(pattern_file)
        self.meta_info = self.read_meta_info()

    def pattern_instance_generator(self, source):
        '''
        tokenize each line in the gazetteer file if the line
            - not a comment line (start with #)
            - contain alphanumber character

        params:
            - source: gz_file

        output:

            - a list of token list, e.g. [['a', 'b'], ['c', 'd', 'e']]

        '''
        with open(source, 'r+', encoding="utf-8") as gz_fh:
            for line in gz_fh:
                line = line.rstrip()
                if self._validate_pattern(line):
                    yield (line, None)

    @staticmethod
    def codeid_description_mapping():
        '''
        no codeid information from gazetteer, output a empty dictionary
        '''
        return dict()

    def _validate_pattern(self, pattern):
        '''
        validate each pattern in the gazetteer/codetable,
        validate if the line is
            - not a comment line (start with #)
            - contain alphanumber character

        params:
            - pattern: (string)

        output:
            - True/False: (binary)
        '''
        valid = True
        if not has_content(pattern):
            valid = False
        return valid

    @staticmethod
    def read_meta_info():
        '''
        no meta info from gazetteer, output a empty dictionary
        '''
        return dict()
