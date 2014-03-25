#!/usr/bin/env python
# -*- coding: utf-8 -*-

from trees.pasparser import *
from operations.flipPos import *
import copy

class T_H:
    def __init__(self, t, h, label=None):
        parser = PASParser()
        self.t = parser.parse(t)
        self.hs = [parser.parse(h),]
        self.label = label
        self.proof = []
        self.__feature = []

    @property
    def feature(self):
        if len(self.__feature) == 0:
            return None
        else:
            return self.__feature
    
    def __getFeature(self):
        self.proof
        return [0, len(self.hs[0])]
    
    def search(self, w, b, k):
        text = self.t # treeのリスト
        hypothes = copy.copy(self.hs[0]) # treeのリスト(参照でなくコピーを操作して，サーチする)
        args = []
        value = FlipPos.getValue(text, hypothes, args)
        self.proof.append([FlipPos(), args])
        
        
        self.__feature = self.__getFeature()

    def translate(self):
        if len(self.proof) == 0:
            raise Exception("proofがないです")
        for items in self.proof:
            oper = items[0]
            args = items[1]
            oper.translateT_H(self, args)
