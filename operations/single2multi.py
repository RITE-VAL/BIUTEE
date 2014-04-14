#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operation import *

class Single2Multi(Operation):

    @classmethod
    def getValue(cls, t, h, w, b, args=None):
        return -1

    @classmethod
    def getKBest(cls, t, h , args, w, b, k):
        valueList = []
        for index in args["selfNodeIndexDic"].keys():
            for word, prob in args["vocabDic"].items:
                arg["selfNodeIndex"] = index
                arg["word"] = word
                valueList.append([self.getValue(t, h, w, b, arg), arg])
    
    @classmethod
    def transFormTree(cls, h, args=None):
        word = arg["word"]
        selfNodeIndex = arg["selfNodeIndex"]
        h[0].insert_node(word, selfNodeIndex)
    
    @classmethod
    def transFormT_H(cls, t_h, args=None):
        word = arg["word"]
        selfNodeIndex = arg["selfNodeIndex"]
        t_h.hs.append( [t_h.hs[len(t_h.hs) - 1][0].insert_node(word, selfNodeIndex),] )
