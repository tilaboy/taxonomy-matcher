"""unit tests to load data from different data resource"""
# -*- coding: utf-8 -*-
from unittest import TestCase
from taxonomy_matcher.matcher import Matcher

class TrieMatcherTestCases(TestCase):
    def setUp(self):
        self.nt_file = 'tests/resource/test_normalized_table.json'

    def test_build_from_nt(self):
        taxonomy_matcher = Matcher(normtable=self.nt_file)
        self.assertEqual(taxonomy_matcher.trie_matcher.token_trie,
        {'linked':
            {'server':
                {'xxENDxx': ('linked server', 'KSA8JE6A22KUR2OLU7RG')}
            },
        'build':
            {'script':
                {'xxENDxx': ('build script', 'KSFVUGQPCSO6RS0X07G8')}
            },
        'user':
            {'interface':
                {'programming':
                    {'xxENDxx': ('user interface programming', 'KSHI3HJOWVSR6PGHQ7CA')}
                }
            },
        'ui':
            {'programming':
                {'xxENDxx': ('ui programming', 'KSHI3HJOWVSR6PGHQ7CA')}
            },
        'oracle':
            {'agile':
                {'product':
                    {'lifecycle':
                        {'management':
                            {'xxENDxx': ('oracle agile product lifecycle management', 'KS0W11G2V8ETTQCKOV7S')}
                        }
                    },
                'plm':
                    {'xxENDxx': ('oracle agile plm', 'KS0W11G2V8ETTQCKOV7S')}
                },
            'apache':
                {'mahout':
                    {'xxENDxx': ('oracle apache mahout', 'KSRT0BE62KLQPF7WZC3O')}
                }
            },
        'apache':
            {'mahout':
                {'xxENDxx': ('apache mahout', 'KSRT0BE62KLQPF7WZC3O')}
            },
        'mahout':
            {'xxENDxx': ('Mahout', 'KSRT0BE62KLQPF7WZC3O')},
        'mathematiques':
            {'xxENDxx': ('mathématiques', 'KS126706DPFD3354M7YK')},
        'c++':
            {'xxENDxx': ('c++', 'KS126706DPFD3354M7Y0')}
        }
    )


    def test_nt_trie_match(self):
        taxonomy_matcher = Matcher(normtable=self.nt_file)
        text = '''A build script is required to do the UI programming or so
called user interface programming, the whole process can be managed by applying
Oracle agile product lifecycle management with the help of Orale Apache Mahout
expert (using Oracle agile PLM and MAHOUT).
'''

        self.assertEqual(
            [
                (match.surface_form, match.start_pos,
                match.end_pos, match.code_description)
                for match in list(taxonomy_matcher.matching(text))
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

    def test_empty_surface_form(self):
        """Log error on empty surface form."""

        with self.assertLogs(level='ERROR') as log:
            Matcher("tests/resource/skills-normalization-EN-empty.json")
            self.assertIn("Empty surface form", log.output[0])

    def test_likelihood_from_nt(self):
        """the likelihood with the correct value"""

        taxonomy_matcher = Matcher(normtable=self.nt_file)
        print(taxonomy_matcher.trie_matcher.token_trie)
        text = '''try this: UI programming or Ui Programming, and math tools like
Mathématiques or mathematiques, or mathématiques.'''

        matched_phrases = list(taxonomy_matcher.matching(text))
        print(matched_phrases)
        self.assertEqual(len(matched_phrases), 5)
        self.assertEqual(
            [
                matched_phrase.surface_form
                for matched_phrase in matched_phrases
            ],
            ['UI programming', 'Ui Programming', 'Mathématiques', 'mathematiques', 'mathématiques'],
            'extracted phrases'
        )
        self.assertEqual(
            [
                matched_phrase.skill_likelihood
                for matched_phrase in matched_phrases
            ],
            [0.5, 0.5, 0.4, 0.4, 0.4],
            'skill_likelihood'
        )
