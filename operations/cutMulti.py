#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operation import *

class CutMulti(Operation):

    @classmethod
    def getValue(cls, t, h, w, b, arg=None):
        return -1 * w[cls]

    @classmethod
    def getKBest(cks, t, h, args, w, b, k):
        valueList = []
        for index in args["selfNodeIndexDic"].keys():
            arg["selfNodeIndex"] =  index
            valueList.append([self.getValue(t, h, w, b, arg), arg])
        valueList = sorted(valueList, reverse=True)[:k-1]
        return valueList

    @classmethod
    def transFormTree(cls, h, arg=None):
        h[0].delete_node(arg["selfNodeIndex"])
    
    @classmethod
    def transFormT_H(cls, t_h, arg=None):
        t_h.hs.append( [t_h.hs[len(t_h.hs) - 1][0].delete_node(arg["selfNodeIndex"]),] )
