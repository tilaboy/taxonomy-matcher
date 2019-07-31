'''MatchPatters: module to load GZ/CT/NT to the tokenized patterns'''
import json
from .patterns import Patterns
from .patterns import PatternTypes


class PatternsNT(Patterns):
    '''
    PatternsNT:

    Class to store pattern information from Normalized Code JSON file

    attibutes:

        - codeid_description: a mapping from codeid to description and
          category, e.g. "1020": {"desc": "Arabic", "type": "language_skill"}

        - tokenized_pattern: a tokenized pattern generator
    '''

    def __init__(self, tokenizer, pattern_file):
        super(PatternsNT, self).__init__(tokenizer, pattern_file)
        self.pattern_file_type = PatternTypes.PATTERN_FILE_TYPE_GZ
        pattern_dict = self._load_nt(self.pattern_file)
        self.codeid_description = self.codeid_description_mapping(pattern_dict)
        self.tokenized_pattern = self.pattern_tokens_generator(pattern_dict)
        self.meta_info = self.read_meta_info(pattern_dict)

    @staticmethod
    def _load_nt(pattern_file):
        with open(pattern_file, 'rt', encoding='utf-8') as pattern_fh:
            return json.load(pattern_fh)

    def pattern_instance_generator(self, source):
        '''
        generate the (pattern string, codeid)

        params:
            - source: dictionary loaded from json

        output:
            - the pattern, codeid pairs, e.g. ('java developer', '1024')
        '''

        for record in source['concepts']:
            code_id = record['id']
            for instance in record['surface_forms']:
                yield (instance['surface_form'], code_id)

    @staticmethod
    def codeid_description_mapping(codetable_dict):
        '''
        build the codeid to description and category mapping

        params:
            - codetable_dict: dictionary loaded from json

        output:
            - the dictionry of codeid to description and category

              dict[code_id] = {'desc':code_description, 'type':code_category}
        '''

        id_x_desc_type = dict()
        for concept in codetable_dict['concepts']:
            code_id = concept.get('id', None)
            if code_id is None:
                continue

            code_description = concept.get('display_name', None)
            code_category = concept.get('category', None)
            if code_id in id_x_desc_type:
                assert id_x_desc_type[code_id]['desc'] == code_description
                assert id_x_desc_type[code_id]['type'] == code_category
            else:
                id_x_desc_type[code_id] = {
                    'desc': code_description,
                    'type': code_category,
                    'skill_likelihoods': PatternsNT.surface_form_likelihoods(
                        concept)
                }
        return id_x_desc_type

    @staticmethod
    def surface_form_likelihoods(concept: dict):
        return {
            surface_form_entry["surface_form"]:
                surface_form_entry["skill_likelihood"]
            for surface_form_entry in concept["surface_forms"]
            if "skill_likelihood" in surface_form_entry
        }

    @staticmethod
    def read_meta_info(source):
        '''
        return the meta info of the json format
        '''
        return source['meta']
