import logging

from .token_trie import TokenTrie
from .tokenizer import Tokenizer

from .match_patterns import PatternsGZ
from .match_patterns import PatternsCT
from .match_patterns import PatternsNT
from .matched_phrase import MatchedPhrase
from . import data_utils


class Matcher():
    '''
    Matcher finds all matched phrases from the input text. It contains
        - an internal tokenizer applied on both patterns and input text
        - a token trie structure created eithor from gazetteer or codetable
        - a dictionary to map codeID to code_description and code_category

    Params:
        - normtable: normalized table file in json format
        - gazetteer: gazetteer file
        - codetable: taxonomy codetable format file
        - blacklist: blacklist file
        - with_context: also output the context if set to True
    '''

    # the magic number is related to the average length of the context in the
    # training data
    CONTEXT_LENGTH = 14

    def __init__(
            self,
            normtable=None,
            gazetteer=None,
            codetable=None,
            blacklist=None,
            regexp=None,
            with_context=False
    ):
        self.regexp = regexp
        self.tokenizer = Tokenizer(self.regexp)
        self.blacklist = dict()
        self.with_context = with_context

        if normtable:
            match_patterns = PatternsNT(self.tokenizer, normtable)
        elif gazetteer:
            match_patterns = PatternsGZ(self.tokenizer, gazetteer)
        elif codetable:
            match_patterns = PatternsCT(self.tokenizer, codetable)
        else:
            raise Exception('source file is required to build a \
            Matcher object')

        self.code_property_mapping = match_patterns.codeid_description
        self.meta_info = match_patterns.meta_info

        if blacklist:
            self.blacklist = data_utils.from_file_to_list(blacklist)

        self.trie_matcher = TokenTrie(
            patterns=match_patterns.tokenized_pattern
        )

    def matching(self, text):
        '''
        find all matching phrases from the input text

        params:
            - text: string

        output:
            - all matching phrases as MatchedPhrase object
        '''
        tokens = self.tokenizer.tokenize_with_pos_info(text)
        for token in tokens:
            token.text = data_utils.normalize(token.text)
        idx = 0
        nr_tokens = len(tokens)
        while idx < nr_tokens:
            local_match = self.trie_matcher.longest_match_at_position(
                self.trie_matcher.token_trie, tokens[idx:])

            if local_match:
                start_pos, end_pos = local_match.text_range()
                left_context, right_context = self.prepare_context(
                    tokens, local_match, idx, text)
                surface_form = local_match.pattern_form()
                yield MatchedPhrase(
                    surface_form,
                    text[start_pos:end_pos],
                    start_pos,
                    end_pos - 1,  # prepare for the entity fromwork (in perl)
                    local_match.code_id,
                    self.code_id_property_lookup(local_match.code_id, 'desc'),
                    self.code_id_property_lookup(local_match.code_id, 'type'),
                    left_context,
                    right_context,
                    self.code_id_property_lookup(
                        local_match.code_id, 'skill_likelihoods', dict()
                    ).get(surface_form, None),
                )
                idx += len(local_match.tokens)
            else:
                idx += 1

    def prepare_context(self, tokens, local_match, idx, text):
        l_context = ''
        r_context = ''
        if self.with_context:
            nr_matched_tokens = len(local_match.tokens)
            l_context_begin = max(0, idx - self.CONTEXT_LENGTH)
            l_context_end = idx
            r_context_begin = idx + nr_matched_tokens
            r_context_end = min(
                len(tokens),
                r_context_begin + self.CONTEXT_LENGTH
            )
            if l_context_begin < l_context_end:
                l_context = text[tokens[l_context_begin].start_pos:
                                 tokens[l_context_end - 1].end_pos]
            if r_context_begin < r_context_end:
                r_context = text[tokens[r_context_begin].start_pos:
                                 tokens[r_context_end - 1].end_pos]
        return l_context, r_context

    def code_id_property_lookup(self, code_id, property_name, default=None):
        code_property = default
        if code_id is not None:
            if code_id in self.code_property_mapping:
                code_property = self.code_property_mapping[code_id].get(
                    property_name, default)
            else:
                logging.warning(
                    'WARNING: no property {} for codeid: {}'.
                    format(property_name, code_id)
                )
        return code_property
