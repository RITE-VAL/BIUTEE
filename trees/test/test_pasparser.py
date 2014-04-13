# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
import pasparser
import tree
import node


class TestPASParser(unittest.TestCase):

    def setUp(self):
        self.chapas_parser = pasparser.PASParser()
        self.ins1 = self.chapas_parser.parse("花子は太郎にプレゼントをあげた")
        self.ins2 = self.chapas_parser.parse("花子は果物屋に行った．\nそこで林檎を買った．")
        self.c1 = pasparser.chapas("花子は太郎にプレゼントをあげた").rstrip()
        self.c2 = pasparser.chapas("花子は果物屋に行った．\nそこで林檎を買った．").rstrip()

    def test_chapas1(self):
        a = unicode(open('test/testchapas1.txt').read(), 'UTF-8').rstrip()
        self.assertEqual(unicode(self.c1, 'UTF-8'), a)

    def test_chapas2(self):
        a = unicode(open('test/testchapas2.txt').read(), 'UTF-8').rstrip()
        self.assertEqual(unicode(self.c2, 'UTF-8'), a)

    def test_pas1_trees(self):
        self.assertEqual(len(self.ins1), 1)
        self.assertTrue(isinstance(self.ins1[0], tree.Tree))

    def test_pas1_tree(self):
        tree1 = self.ins1[0]
        self.assertEqual(len(tree1), 4)
        for n in tree1:
            self.assertTrue(isinstance(tree1[n], node.Node))

    def test_pas1_node(self):
        tree1 = self.ins1[0]
        txt = ""
        for n, c in zip(tree1, [2, 2, 2, 2]):
            self.assertEqual(len(tree1[n]), c)
            txt += tree1[n].get_surface()
        self.assertEqual(u"花子は太郎にプレゼントをあげた", txt)

    def test_pas2_node(self):
        tree1 = self.ins2[0]
        tree2 = self.ins2[1]
        txt = u""
        for n, c in zip(tree1, [2, 3, 3]):
            self.assertEqual(len(tree1[n]), c)
            txt += tree1[n].get_surface()
        self.assertEqual(u"花子は果物屋に行った．", txt)
        txt = u""
        for n, c in zip(tree2, [1, 2, 3]):
            self.assertEqual(len(tree2[n]), c)
            txt += tree2[n].get_surface()
        self.assertEqual(u"そこで林檎を買った．", txt)

    def test_pas2_trees(self):
        tree1 = self.ins2[0]
        tree2 = self.ins2[1]
        self.assertEqual(len(tree1), 3)
        for n in tree1:
            self.assertTrue(isinstance(tree1[n], node.Node))
        self.assertEqual(len(tree2), 3)
        for n in tree2:
            self.assertTrue(isinstance(tree1[n], node.Node))


if __name__ == '__main__':
    unittest.main()
