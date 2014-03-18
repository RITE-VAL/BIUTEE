# -*- coding: utf-8 -*-

import unittest
import node
import pasparser


class TestTree(unittest.TestCase):

    def setUp(self):
        pass

    def test_node1(self):
        n = node.Node(u"* 0 2D 0/1 -2.018984", pasparser.parse_cabocha_header)
        self.assertEqual(n.dependance, 2)
        self.assertEqual(n.subject, 0)
        self.assertEqual(n.funcword, 1)

    def test_node2(self):
        n = node.Node(u"* 0 2D 0/0 -1.497410", pasparser.parse_cabocha_header)
        self.assertTrue(n.dependance == 2)
        self.assertTrue(n.subject == 0)
        self.assertTrue(n.funcword == 0)

    def test_node3(self):
        n = node.Node(u"* 2 -1D 0/1 0.000000", pasparser.parse_cabocha_header)
        self.assertTrue(n.dependance == -1)
        self.assertTrue(n.subject == 0)
        self.assertTrue(n.funcword == 1)


if __name__ == '__main__':
    unittest.main()
