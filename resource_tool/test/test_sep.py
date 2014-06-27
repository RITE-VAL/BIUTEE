# -*- coding: utf-8 -*-
import unittest
from sentence_split import sentence_split


class TestSep(unittest.TestCase):

    def setUp(self):
        self.text1 = u'第１回総選挙のころ，政府を支持する政党は吏党とよばれた。'
        self.text2 = u'吏党（りとう）とは、明治時代中期の初期帝国議会における' \
                     u'政府寄りの姿勢を示した政党のこと。ただし、本来は自由民権運動' \
                     u'を継承する民党側からの蔑称であり、政府・マスコミおよび' \
                     u'当事者達は温和派（おんわは）と呼称していた。'
        self.text3 = u'''テキスト（英語: text、ドイツ語: Text、フランス語: texte）は、文章や文献のひとまとまりを指して呼ぶ呼称。 言葉によって編まれたもの、という含みを持つ語で、織物（Textile テクスタイル）と同じくラテン語の「織る」が語源である。
ほかに日本語では、英語: textbook 「テキストブック、教科書」の略称としても使われる。'''

    def test_sp1(self):
        self.assertEqual(sentence_split(self.text1), [self.text1])

    def test_sp2(self):
        ss = sentence_split(self.text2)
        self.assertEqual(
            ss,
            sentence_split(self.text2), [
                u'吏党（りとう）とは、明治時代中期の初期帝国議会における政府寄りの姿勢を示した政党のこと。',
                u'ただし、本来は自由民権運動を継承する民党側からの蔑称であり、'
                u'政府・マスコミおよび当事者達は温和派（おんわは）と呼称していた。'
            ]
        )

    def test_sp3(self):
        ss = sentence_split(self.text3)
        self.assertEqual(ss, [
            u'テキスト（英語: text、ドイツ語: Text、フランス語: texte）は、文章や文献のひとまとまりを指して呼ぶ呼称。',
            u' 言葉によって編まれたもの、という含みを持つ語で、織物（Textile テクスタイル）と同じくラテン語の「織る」が語源である。',
            u'ほかに日本語では、英語: textbook 「テキストブック、教科書」の略称としても使われる。'
        ])


if __name__ == '__main__':
    unittest.main()
