#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operation import *

class CutMulti(Operation):

    @classmethod
    def getValue(cls, t, h, w, b, args=None):
        return -1 * w[cls]

    @classmethod
    def getKBest(cks, t, h, args, w, b, k):
        valueList = []
        for index in args["selfNodeIndex"]:
            arg["selfNodeIndex"] =  index
            valueList.append([self.getValue(t, h, w, b, arg), arg])
        valueList = sorted(ValueList, reverse=True)[:k-1]
        return valueList

    @classmethod
    def transFormTree(cls, h, args=None):
        h[0].flip_part_of_speech()
    
    @classmethod
    def transFormT_H(cls, t_h, args=None):
        t_h.hs.append( [t_h.hs[len(t_h.hs) - 1][0].flip_part_of_speech(),] )
