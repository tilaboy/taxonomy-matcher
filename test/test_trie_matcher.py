"""unit tests to load data from different data resource"""
from unittest import TestCase
from gz_matcher.token_trie import TokenTrie

class TrieMatcherTestCases(TestCase):
    def setUp(self):
        self.gz_file = 'test/resource/gazetteer.txt'
        self.text_1 = 'ab Foo bar Foo foo chao foo\nBar    foo bar foo foo'
        self.text_2 = 'ab Foo Foo foo foo\nBar     bar foo foo'
        self.real_gz_file = 'test/resource/compskill.txt'
        with open('test/resource/cv1.xml') as input_fh:
            self.real_cv = input_fh.read()

    def test_trie_match(self):
        token_trie = TokenTrie.build_from_gz(self.gz_file)
        all_matches_1 = list(token_trie.search_matches(self.text_1))

        self.assertEqual(all_matches_1, [
                ('foo bar foo', 3, 13),
                ('chao', 19, 22),
                ('foo bar foo', 24, 37),
                ('bar foo foo', 39, 49)])

        all_matches_2 = list(token_trie.search_matches(self.text_2))
        self.assertEqual(all_matches_2, [
                ('foo bar', 15, 21),
                ('bar foo foo', 27, 37)])

    def test_on_real_file(self):
        token_trie = TokenTrie.build_from_gz(self.real_gz_file)
        all_matches = list(token_trie.search_matches(self.real_cv))
        self.assertEqual(all_matches, [
        ('c', 278, 278), ('transportation', 590, 603),
        ('c', 727, 727), ('benchmarking', 762, 773), ('c', 816, 816),
        ('project management', 934, 951), ('class', 1190, 1194),
        ('skills', 1233, 1238), ('korn', 1845, 1848),
        ('logistics', 1918, 1926), ('express', 2042, 2048),
        ('express', 2095, 2101), ('wide', 2347, 2350),
        ('benchmarking', 2703, 2714), ('wide', 2727, 2730),
        ('wide', 2918, 2921), ('development process', 2949, 2988),
        ('wide', 3109, 3112), ('express', 3249, 3255),
        ('express', 3347, 3353), ('process management', 3569, 3586),
        ('express', 3598, 3604), ('express', 3677, 3683),
        ('c', 3709, 3709), ('benchmarking', 3819, 3830),
        ('express', 3963, 3969), ('express', 4201, 4207),
        ('rational', 4248, 4255), ('express', 4283, 4289),
        ('network', 4390, 4396), ('express', 4412, 4418),
        ('express', 4455, 4461), ('c', 4540, 4540), ('sa', 4592, 4593),
        ('sales', 4992, 4996), ('sales', 7171, 7175),
        ('incentive programs', 7288, 7305), ('sales', 7336, 7340),
        ('sales', 7479, 7483), ('training', 7617, 7624),
        ('functions', 8004, 8012), ('education', 8707, 8715),
        ('marketing', 8756, 8764), ('sales', 8772, 8776),
        ('class', 8898, 8902), ('mathematics', 9148, 9158),
        ('physics', 9166, 9172), ('skills', 9200, 9205),
        ('ms office', 9255, 9263), ('visio', 9330, 9334)])
