'''
MatchedPhrase:

matched phrases found from text can be saved as MatchedPhrase object.
Apart from the matched phrase itself, the object also add information
like postion, matched code, and context info.'''


class MatchedPhrase:
    '''
    each matched phrase must have the following infor:
    - (normalized) matching pattern
    - surface form
    - start position in the original text
    - end position in the original text

    depending on the input, it could have
    - code_id
    - code_description
    - category
    '''

    def __init__(self,
                 matched_pattern=None,
                 surface_form=None,
                 start_pos=None,
                 end_pos=None,
                 code_id=None,
                 code_description=None,
                 code_category=None,
                 left_context=None,
                 right_context=None,
                 skill_likelihood=None
                 ):
        self.matched_pattern = matched_pattern
        self.surface_form = surface_form
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.code_id = code_id
        self.code_description = code_description
        self.category = code_category
        self.left_context = left_context
        self.right_context = right_context
        self.skill_likelihood = skill_likelihood

    def __repr__(self):
        return '''found:
        skill: {}
        surface_form: {}
        range: [{}:{}]
        codeid:{}
        description: {}
        category: {}
        skill likelihood: {}'''.format(
            self.matched_pattern,
            self.surface_form,
            self.start_pos,
            self.end_pos,
            self.code_id,
            self.code_description,
            self.category,
            self.skill_likelihood
        )
