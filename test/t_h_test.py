#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from t_h import *
from operations.flipPos import *
from trees.pasparser import *


class T_HClassTestCase(unittest.TestCase):
    def setUp(self):
        self.myT_H = T_H("こんにちは", "こんにちは", 1)

    def testSearch(self):
        proof = [[FlipPos(), []],]
        self.myT_H.search(1, 1, 1)
        self.assertListEqual(proof, self.myT_H.proof)
        feature = [1,1,1,0,0.2]
        self.assertListEqual(feature, self.myT_H.feature)

    def testTranslate(self):
        self.myT_H.search(1, 1, 1)
        self.myT_H.translate()
        self.assertListEqual(self.myT_H.t, self.myT_H.hs[len(self.myT_H.hs) - 1])

if __name__ == '__main__':
    unittest.main()
