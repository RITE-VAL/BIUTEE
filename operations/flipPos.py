#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operation import *

class FlipPos(Operation):

    @classmethod
    def getValue(cls, t, h, w, b, arg=None):
        return -1 * w[cls]

    @classmethod
    def getKBest(cls, t, h , args, w, b, k):
        valueList = []
        for index in args["selfNodeIndex"]:
            for relation in args["relationList"]:
                arg["selfNodeIndex"] = index
                arg["relationList"] = relation
                valueList.append([self.getValue(t, h, w, b, arg), arg])
        valueList = sorted(ValueList, reverse=True)[:k-1]
        return valueList

    @classmethod
    def transFormTree(cls, h, arg=None):
        h[0].flip_part_of_speech()
    
    @classmethod
    def transFormT_H(cls, t_h, arg=None):
        t_h.hs.append( [t_h.hs[len(t_h.hs) - 1][0].flip_part_of_speech(),] )
