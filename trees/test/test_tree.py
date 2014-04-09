# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
import pasparser


class TestTree(unittest.TestCase):

    def setUp(self):
        self.chapas_parser = pasparser.PASParser()
        self.c1 = pasparser.chapas("花子は太郎にプレゼントをあげた").rstrip()
        self.c2 = pasparser.chapas("花子は果物屋に行った．\nそこで林檎を買った．").rstrip()

    def test_tree1(self):
        pass

    def test_tree2(self):
        pass

    def test_tree3(self):
        pass


if __name__ == '__main__':
    unittest.main()
