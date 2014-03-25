#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import unittest
from flipPos import *
from t_h import *
from trees.pasparser import *

class testFlipPos(unittest.TestCase):

    def testGetValue(self):
        t = PASParser().parse("こんにちは，太郎")
        h = PASParser().parse("こんにちは")
        self.assertEqual(-1, FlipPos.getValue([1,2], t, h))
    
    def testTranslateTree(self):
        h = PASParser().parse("こんにちは")
        FlipPos.translateTree(h, [1,0])
        self.assertListEqual(h, h)

    def testTranslateT_H(self):
        t_h = T_H("こんにちは", "こんにちは", 1)
        FlipPos.translateT_H(t_h, [1,0])
        test = PASParser().parse("こんにちは")
        self.assertListEqual(t_h.hs[len(t_h.hs) -1], test)

if __name__ == '__main__':
    unittest.main()
