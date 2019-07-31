'''MatchPatters: module to load GZ/CT/NT to the tokenized patterns'''
import xml.etree.ElementTree as ET
from taxonomy_matcher.data_utils import fetch_node_text
from .patterns import Patterns
from .patterns import PatternTypes


class PatternsCT(Patterns):
    '''
    PatternsCT:

    Class to store pattern information from Taxonomy Codetable

    attibutes:

        - codeid_description: a mapping from codeid to description and
          category, e.g. "1020": {"desc": "Arabic", "type": "language_skill"}

        - tokenized_pattern: a tokenized pattern generator
    '''
    def __init__(self, tokenizer, pattern_file):
        super(PatternsCT, self).__init__(tokenizer, pattern_file)
        self.pattern_file_type = PatternTypes.PATTERN_FILE_TYPE_GZ
        tree_root = self._load_ct(self.pattern_file)
        self.codeid_description = self.codeid_description_mapping(tree_root)
        self.tokenized_pattern = self.pattern_tokens_generator(tree_root)
        self.meta_info = self.read_meta_info()

    @staticmethod
    def _load_ct(pattern_file):
        pattern_tree = ET.parse(pattern_file)
        return pattern_tree.getroot()

    def pattern_instance_generator(self, source):
        '''
        generate the (pattern string, codeid)

        params:
            - source: ElementTree root object

        output:
            - the pattern, codeid pairs, e.g. ('java developer', '1024')

        '''

        for record in source.find('CodeRecordList'):
            code_id = record.find('CodeID').text
            for instance in record.iter('InstanceDescription'):
                yield (instance.text, code_id)

    @staticmethod
    def codeid_description_mapping(codetable_root):
        '''
        build the codeid to description and category mapping

        params:

            - codetable_root: ElementTree root object

        output:

            - the dictionry of codeid to description and category

              dict[code_id] = {'desc':code_description, 'type':code_category}

        '''

        id_x_desc_type = dict()
        for record in codetable_root.find('CodeRecordList'):
            code_id = fetch_node_text(record, 'CodeID')
            if code_id is None:
                continue

            code_description = fetch_node_text(record, 'CodeDescription')
            code_category = fetch_node_text(
                record,
                "CodeProperty[@name='skill_type']"
            )

            if code_id in id_x_desc_type:
                assert id_x_desc_type[code_id]['desc'] == code_description
                assert id_x_desc_type[code_id]['type'] == code_category
            else:
                id_x_desc_type[code_id] = {
                    'desc': code_description,
                    'type': code_category
                }
        return id_x_desc_type

    @staticmethod
    def read_meta_info():
        '''
        The meta_info for the codetable is not implemented, output a empty
        dictionary
        '''
        return dict()
