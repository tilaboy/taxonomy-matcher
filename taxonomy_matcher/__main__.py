'''
taxonomy_match: script to load a taxonomy, and find all matches from input
'''

from argparse import ArgumentParser
from .matcher import Matcher
from . import LOGGER


def get_args():
    '''get arguments'''
    parser = ArgumentParser(description='find matched phrases from input text')

    parser.add_argument('input_file', help='''input text file''', type=str)

    tax_args = parser.add_mutually_exclusive_group(required=True)

    tax_args.add_argument('--json_tax',
                          help='normalization taxonomy in json form',
                          type=str, default='')

    tax_args.add_argument('--xml_tax', help='taxonomy in xml form',
                          type=str, default='')
    tax_args.add_argument('--gz_tax', help='a list of keywords in txt form',
                          type=str, default='')

    return parser.parse_args()


def main():
    '''apply selectors to xml files'''
    args = get_args()

    with open(args.input_file, "r", encoding="utf-8") as input_f:
        input_text = input_f.read()

    if args.json_tax:
        taxonomy_matcher = Matcher(normtable=args.json_tax)
    elif args.xml_tax:
        taxonomy_matcher = Matcher(codetable=args.xml_tax)
    elif args.gz_tax:
        taxonomy_matcher = Matcher(gazetteer=args.gz_tax)

    for matched in taxonomy_matcher.matching(input_text):
        LOGGER.info(matched)
