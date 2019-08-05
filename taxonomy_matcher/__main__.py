'''
taxonomy_match: script to load a taxonomy, and find all matches from input
'''
import os.path
from argparse import ArgumentParser
from .matcher import Matcher
from . import LOGGER
from .data_saver import DataSaver


def get_args():
    '''get arguments'''
    parser = ArgumentParser(description='''
                            load taxonomy phrases from the taxonomy file, and
                            find all matched phrases from the input text. The
                            result will eithor write to an output file or print
                            to the screen.
                            ''')

    parser.add_argument('input_file', help='input file with text ', type=str)

    parser.add_argument('taxonomy_file', help='''
                        taxonomy file, support json/xml/txt, see documentation
                        for more details
                        ''', type=str)

    parser.add_argument('--output_file', help='''
                        output file of matched phrases, supports
                        jsonl/csv/tsv/txt format''',
                        type=str, default='STDOUT')

    return parser.parse_args()


def _init_matcher_obj(taxonomy_file):
    if not os.path.isfile(taxonomy_file):
        raise FileNotFoundError("Taxonomy file not found")

    _, extension = os.path.splitext(taxonomy_file)

    if extension == '.json':
        taxonomy_matcher = Matcher(normtable=taxonomy_file)
    elif extension == '.xml':
        taxonomy_matcher = Matcher(codetable=taxonomy_file)
    elif extension == '.txt':
        taxonomy_matcher = Matcher(gazetteer=taxonomy_file)
    else:
        raise ValueError("Only support taxonomy in json/xml/txt")

    return taxonomy_matcher


def main():
    '''
    taxonomy-match

    params:

    - input_file: text document to extract keywords

    - taxonomy_file: taxonomy contains keywords

    output: output_file
    '''
    args = get_args()

    LOGGER.info('Loading text file')
    with open(args.input_file, "r", encoding="utf-8") as input_f:
        input_text = input_f.read()

    LOGGER.info('Loading the Taxonomy ...')
    taxonomy_matcher = _init_matcher_obj(args.taxonomy_file)
    writer = DataSaver(args.output_file)

    nr_matches = 0
    for matched in taxonomy_matcher.matching(input_text):
        if writer.format == '.csv' or writer.format == '.tsv':
            if nr_matches == 0:
                writer.store(matched._to_dict().keys())
            writer.store(matched._to_list())

        elif writer.format == '.jsonl':
            writer.store(matched._to_dict())
        else:
            writer.store(matched)

        nr_matches += 1

    LOGGER.info('found %i matched phrases', nr_matches)
