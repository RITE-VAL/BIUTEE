# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
import node
import pasparser


class TestNode(unittest.TestCase):

    def setUp(self):
        pass

    def test_node1(self):
        n = node.Node(2, 0, 1)
        self.assertEqual(n.parent, 2)
        self.assertEqual(n.subject, 0)
        self.assertEqual(n.funcword, 1)

    def test_node2(self):
        n = node.Node(2, 0, 0)
        self.assertEqual(n.parent, 2)
        self.assertEqual(n.subject, 0)
        self.assertEqual(n.funcword, 0)

    def test_node3(self):
        n = node.Node()
        self.assertEqual(n.parent, None)
        self.assertEqual(n.subject, None)
        self.assertEqual(n.funcword, None)

    def test_add_word(self):
        n = node.Node(2, 0, 0)
        n.add_word(node.Word())
        n.add_word(node.Word())
        self.assertEqual(len(n), 2)


class TestWord(unittest.TestCase):

    def setUp(self):
        pass

    def test_word1(self):
        i = pasparser.parse_cabocha_node(
            "果物\t名詞,一般,*,*,*,*,果物,クダモノ,クダモノ\tO"
        )
        n = node.Word(i)
        self.assertEqual(n.ne, None)
        self.assertEqual(n.string, u'果物')
        self.assertEqual(n.pos, u'名詞')
        self.assertEqual(n.subpos, u'一般')
        self.assertEqual(n.pas, None)

    def test_word2(self):
        i = pasparser.parse_cabocha_node(
            ('行っ\t動詞,自立,*,*,五段・カ行促音便,'
             '連用タ接続,行く,イッ,イッ\tO\ttype="pred" ga="1" ni="2"')
        )
        n = node.Word(i)
        self.assertEqual(n.ne, None)
        self.assertEqual(n.string, u'行っ')
        self.assertEqual(n.pos, u'動詞')
        self.assertEqual(n.subpos, u'自立')
        self.assertEqual(n.pas, u'type="pred" ga="1" ni="2"')

    def test_node3(self):
        n = node.Word(
            pasparser.parse_cabocha_node(
                '花子\t名詞,固有名詞,人名,名,*,*,花子,ハナコ,ハナコ\tB-PERSON\tID="1"'
            )
        )
        self.assertEqual(n.ne, u"B-PERSON")
        self.assertEqual(n.string, u'花子')
        self.assertEqual(n.pos, u'名詞')
        self.assertEqual(n.subpos, u'固有名詞')
        self.assertEqual(n.pas, u'ID="1"')

if __name__ == '__main__':
    unittest.main()
