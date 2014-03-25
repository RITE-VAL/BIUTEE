#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dataPath = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "./test_data.txt"))
import unittest
from machineLearning import *
from t_h import *

class MLClassTestCase(unittest.TestCase):
    def setUp(self):
        self.myML = ML()

    def test_getWeight(self):
        self.assertListEqual([[0.19999999999999998, -0.99, 0.19999999999999998], -0.82], self.myML._ML__getWeight("/home/miura/libsvm-3.17/python/test"))
    
    def test_train(self):
        self.assertListEqual([1, 1], self.myML.train(dataPath, 1, 1, 2))

if __name__ == '__main__':
    unittest.main()
