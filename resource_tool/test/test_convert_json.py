# -*- coding: utf-8 -*-
import unittest
from get_document.convert_json import convert_json


class TestConvertjson(unittest.TestCase):

    def setUp(self):
        self.raw1 = u"温泉卵では熱凝固を起こす温度が卵黄のほうが低いことを利用する。"
        self.text1 = open("test1.knp").read().decode("utf-8")
        self.nn1 = u"END\n"
        self.raw2 = u"1個の細胞に複数のウイルスが感染したとき，増殖は抑制される。"
        self.text2 = open("test2.knp").read().decode("utf-8")
        self.nn2 = u"numerical*1個*0*2*個*1*1*\nEND\n"
        self.simple1 = convert_json(self.raw1, self.text1, self.nn1)
        print self.simple1["knp"]
        self.simple2 = convert_json(self.raw2, self.text2, self.nn2)
        print self.simple2["knp"]

    def test_keys(self):
        self.assertEqual(sorted(self.simple1.keys()),
                         sorted(["nn", "raw_text", "knp", "simple",
                                 "zunda", "chunks"]))
        self.assertEqual(sorted(self.simple2.keys()),
                         sorted(["nn", "raw_text", "knp", "simple",
                                 "zunda", "chunks"]))

    def test_nn(self):
        self.assertEqual(self.simple1["nn"], [])
        self.assertEqual(self.simple2["nn"], [{
            "type": u"numerical",
            "expression": u"1個",
            "start": 0,
            "end": 2,
            "unit": u"個",
            "lower": u"1",
            "upper": u"1",
            "opt": u""
        }])


if __name__ == '__main__':
    unittest.main()
