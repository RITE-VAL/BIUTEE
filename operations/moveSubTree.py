#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operation import *

class MoveSubTree(Operation):

    @classmethod
    def getValue(cls, t, h, w, b, args=None):
        return -1

    @classmethod
    def getKBest(cls, t, h , args, w, b, k):
        valueList = []
        for selfIndex in args["selfNodeIndexDic"].keys():
            for parentIndex in args["parentIndexList"]:
                arg["selfNodeIndex"] = index
                arg["depLabel"] = relation
                valueList.append([self.getValue(t, h, w, b, arg), arg])
    
    @classmethod
    def transFormTree(cls, h, args=None):
        h[0].flip_part_of_speech()
    
    @classmethod
    def transFormT_H(cls, t_h, args=None):
        t_h.hs.append( [t_h.hs[len(t_h.hs) - 1][0].flip_part_of_speech(),] )
