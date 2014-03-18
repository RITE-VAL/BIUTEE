# -*- coding: utf-8 -*-

import unittest
import node
import pasparser


class TestNode(unittest.TestCase):

    def setUp(self):
        pass

    def test_node1(self):
        n = node.Node(u"* 0 2D 0/1 -2.018984", pasparser.parse_cabocha_header)
        self.assertEqual(n.dependance, 2)
        self.assertEqual(n.subject, 0)
        self.assertEqual(n.funcword, 1)
        self.assertEqual(len(n), 0)

    def test_node2(self):
        n = node.Node(u"* 0 2D 0/0 -1.497410", pasparser.parse_cabocha_header)
        self.assertEqual(n.dependance, 2)
        self.assertEqual(n.subject, 0)
        self.assertEqual(n.funcword, 0)
        self.assertEqual(len(n), 0)

    def test_node3(self):
        n = node.Node(u"* 2 -1D 0/1 0.000000", pasparser.parse_cabocha_header)
        self.assertEqual(n.dependance, -1)
        self.assertEqual(n.subject, 0)
        self.assertEqual(n.funcword, 1)
        self.assertEqual(len(n), 0)

    def test_node4(self):
        n = node.Node(line="ROOT", parser=lambda x: x)
        self.assertEqual(n.dependance, None)
        self.assertEqual(n.subject, None)
        self.assertEqual(n.funcword, None)
        self.assertEqual(len(n), 1)


class TestWord(unittest.TestCase):

    def setUp(self):
        pass

    def test_word1(self):
        n = node.Word(u"果物\t名詞,一般,*,*,*,*,果物,クダモノ,クダモノ\tO",
                      pasparser.parse_cabocha_node)
        self.assertEqual(n.ne, None)
        self.assertEqual(n.string, u'果物')
        self.assertEqual(n.pos, u'名詞')
        self.assertEqual(n.subpos, u'一般')
        self.assertEqual(n.pas, None)

    def test_word2(self):
        n = node.Word(
            (u'行っ\t動詞,自立,*,*,五段・カ行促音便,'
             u'連用タ接続,行く,イッ,イッ\tO\ttype="pred" ga="1" ni="2"'),
            pasparser.parse_cabocha_node
        )
        self.assertEqual(n.ne, None)
        self.assertEqual(n.string, u'行っ')
        self.assertEqual(n.pos, u'動詞')
        self.assertEqual(n.subpos, u'自立')
        self.assertEqual(n.pas, u'type="pred" ga="1" ni="2"')

    def test_node3(self):
        n = node.Word(
            '花子\t名詞,固有名詞,人名,名,*,*,花子,ハナコ,ハナコ\tB-PERSON\tID="1"',
            pasparser.parse_cabocha_node
        )
        self.assertEqual(n.ne, u"B-PERSON")
        self.assertEqual(n.string, u'花子')
        self.assertEqual(n.pos, u'名詞')
        self.assertEqual(n.subpos, u'固有名詞')
        self.assertEqual(n.pas, u'ID="1"')

if __name__ == '__main__':
    unittest.main()
