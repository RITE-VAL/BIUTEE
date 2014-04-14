# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
import pasparser


class TestTree(unittest.TestCase):

    def setUp(self):
        '''
        c1[0] -> あげた -> 花子は, 太郎に, プレゼントを
        c2[0] -> 行った． -> 花子は 果物屋に
        c2[0] -> 買った． -> そこで 林檎を
        '''
        self.chapas_parser = pasparser.PASParser()
        self.c1 = self.chapas_parser.parse("花子は太郎にプレゼントをあげた")
        self.c2 = self.chapas_parser.parse("花子は果物屋に行った．\nそこで林檎を買った．")

    def test_tree_len(self):
        self.assertEqual(len(self.c1[0]), 4)
        self.assertEqual(len(self.c2[0]), 3)
        self.assertEqual(len(self.c2[1]), 3)

    def test_tree_poss(self):
        self.assertEqual(sorted(self.c1[0].keys()), [0, 1, 2, 3])
        self.assertEqual(sorted(self.c2[0].keys()), [0, 1, 2])
        self.assertEqual(sorted(self.c2[1].keys()), [0, 1, 2])

    def test_tree_root(self):
        self.assertEqual(self.c1[0].root_pos, 3)
        self.assertEqual(self.c2[0].root_pos, 2)
        self.assertEqual(self.c2[1].root_pos, 2)

    def test_tree_node_children(self):
        self.assertEqual(self.c1[0][0].children, set([]))
        self.assertEqual(self.c1[0][1].children, set([]))
        self.assertEqual(self.c1[0][2].children, set([]))
        self.assertEqual(self.c1[0][3].children, set([0, 1, 2]))

        self.assertEqual(self.c2[0][0].children, set([]))
        self.assertEqual(self.c2[0][1].children, set([]))
        self.assertEqual(self.c2[0][2].children, set([0, 1]))
        self.assertEqual(self.c2[1][0].children, set([]))
        self.assertEqual(self.c2[1][1].children, set([]))
        self.assertEqual(self.c2[1][2].children, set([0, 1]))

    def test_tree_node_rel(self):
        self.assertEqual(self.c1[0][0].rel, {})
        self.assertEqual(self.c1[0][1].rel, {})
        self.assertEqual(self.c1[0][2].rel, {1: "ni"})
        self.assertEqual(self.c1[0][3].rel, {0: "ga", 2: "o"})

        self.assertEqual(self.c2[0][0].rel, {})
        self.assertEqual(self.c2[0][1].rel, {})
        self.assertEqual(self.c2[0][2].rel, {0: "ga", 1: "ni"})
        self.assertEqual(self.c2[1][0].rel, {})
        self.assertEqual(self.c2[1][1].rel, {})
        self.assertEqual(self.c2[1][2].rel, {1: "o"})

    def test_add_to_tree(self):
        pass

    def test_search_word(self):
        self.assertEqual(self.c1[0].search_word(u"花子"), 0)
        self.assertEqual(self.c1[0].search_word(u"太郎"), 1)
        self.assertEqual(self.c1[0].search_word(u"プレゼント"), 2)
        self.assertEqual(self.c1[0].search_word(u"あげ"), 3)
        self.assertEqual(self.c1[0].search_word(u"ねこ"), None)

if __name__ == '__main__':
    unittest.main()
