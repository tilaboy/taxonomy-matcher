"""unit tests to load data from different data resource"""
import json
from unittest import TestCase
from taxonomy_matcher.matcher import Matcher

class TrieMatcherTestCases(TestCase):
    def setUp(self):
        self.nt_file = 'tests/resource/test_normalized_table.json'

    def test_build_from_nt(self):
        nt_matcher = Matcher(normtable=self.nt_file)
        self.assertEqual(nt_matcher.trie_matcher.token_trie,
        {'linked':
            {'server':
                {'xxENDxx': 'KSA8JE6A22KUR2OLU7RG'}
            },
        'build':
            {'script':
                {'xxENDxx': 'KSFVUGQPCSO6RS0X07G8'}
            },
        'user':
            {'interface':
                {'programming':
                    {'xxENDxx': 'KSHI3HJOWVSR6PGHQ7CA'}
                }
            },
        'ui':
            {'programming':
                {'xxENDxx': 'KSHI3HJOWVSR6PGHQ7CA'}
            },
        'oracle':
            {'agile':
                {'product':
                    {'lifecycle':
                        {'management':
                            {'xxENDxx': 'KS0W11G2V8ETTQCKOV7S'}
                        }
                    },
                'plm':
                    {'xxENDxx': 'KS0W11G2V8ETTQCKOV7S'}
                },
            'apache':
                {'mahout':
                    {'xxENDxx': 'KSRT0BE62KLQPF7WZC3O'}
                }
            },
        'apache':
            {'mahout':
                {'xxENDxx': 'KSRT0BE62KLQPF7WZC3O'}
            },
        'mahout':
            {'xxENDxx': 'KSRT0BE62KLQPF7WZC3O'}
        }
    )


    def test_nt_trie_match(self):
        nt_matcher = Matcher(normtable=self.nt_file)
        text = '''A build script is required to do the UI programming or so
called user interface programming, the whole process can be managed by applying
Oracle agile product lifecycle management with the help of Orale Apache Mahout
expert (using Oracle agile PLM and MAHOUT).
'''

        self.assertEqual(
            [
                (match.surface_form, match.start_pos,
                match.end_pos, match.code_description)
                for match in list(nt_matcher.matching(text))
            ],
            [
                ('build script', 2, 13, 'Build Script'),
                ('UI programming', 37, 50, 'User Interface Programming'),
                ('user interface programming', 65, 90,
                'User Interface Programming'),
                ('Oracle agile product lifecycle management',
                 138,
                 178,
                 'Oracle Agile Product Lifecycle Management'),
                ('Apache Mahout', 203, 215, 'Mahout'),
                ('Oracle agile PLM', 231, 246,
                'Oracle Agile Product Lifecycle Management'),
                ('MAHOUT', 252, 257, 'Mahout')
            ]
        )
