#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operation import *
import math

class InsertWord(Operation):

    @classmethod
    def getValue(cls, t, h, w, b, arg=None):
        return math.log(arg["prob"]) * w[cls]

    @classmethod
    def getKBest(cls, t, h , args, w, b, k):
        valueList = []
        for index in args["parenNodeIndexList"]:
            for word, prob in args["vocabDic"].items():
                arg["parentNodeIndex"] = index
                arg["word"] = word
                arg["prob"] = prob
                valueList.append([self.getValue(t, h, w, b, arg), arg])
        valueList = sorted(ValueList, reverse=True)[:k-1]
        return valueList
    
    @classmethod
    def transFormTree(cls, h, arg=None):
         parentNodeIndex = arg["parentNodeIndex"]
         word = arg["word"]
         h[0].insert_node(word, parentNodeIndex)

    @classmethod
    def transFormT_H(cls, t_h, arg=None):
        parentNodeIndex = arg["parentNodeInex"]
        word = arg["word"]
        t_h.hs.appens( [t_h.hs[len(t_h.hs) -1][0].insert_node(word, parentNodeIndex), ] )

