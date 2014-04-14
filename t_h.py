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
    
    def search(self, w, b, k, h=None):
        text = self.t # treeのリスト(リスト要素それぞれが1文を表している)
        hypo = []
        if h == None:
            for i in range(x):
                h = copy.copy(self.hs[0]) # treeのリスト(リスト要素それぞれが1文を表している)(参照でなくコピーを操作して，サーチする)
                hypo.append(h)
        else:
            for i in range(x):
                tmp_h = copy.copy(h)
                hypo.append(tmp_h)

        operationList = [FlipPos, ]

        for o in operationList:
            args = set_args(o)
            # kBest is [[value, ope, arg],[]]
            # tempKBestList is [[value, arg],[]]
            # return of getKBest is k best of the operation
            tempKBestList = o.getKBest(text, hypothesis, args, w, b, k)
            for b in tmpKBestList:
                if b[0] > kBest[3][0]:
                    b.insert(1,o)
                    kBest.append(b)
                    kBest.sort(key=lambda x: x[0], reverse=True)

        # transform a tree
        for i, k in enumerate(kBest):
            o.transformTree(hypo[i], k[2])

            if text == hypo[i]:
                self.proof.append()
                self.__feature = self.__getFeature()
            else:
                search(w, b, k, hypo[i])


    def set_args(self, o):
        parentNodeIndex = extractParentNodeIndex()
        selfNodeIndex = extractSelfNodeIndex()
        depLabel = extractInsertedWord()
        insertedWord =extractInsertedWord()
        return [parentNodeIndex, selfNodeIndex, depLabel, insertedWord]

    def translate(self):
        if len(self.proof) == 0:
            raise Exception("proofがないです")
        for items in self.proof:
            oper = items[0]
            args = items[1]
            oper.translateT_H(self, args)
