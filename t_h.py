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
        text = self.t # treeのリスト(リスト要素それぞれが1文を表している)
        hypothes = copy.copy(self.hs[0]) # treeのリスト(リスト要素それぞれが1文を表している)(参照でなくコピーを操作して，サーチする)
        operationList = [FlipPos, ]
        argsDic = {} # operationごとにargsの設計は違うのでうまいことやってください

        # args elements
        parentNodeIndex = []
        selfNodeIndex = []
        depLabel = []
        insertedWord = []

        argsDic[FlipPos] = [parentNodeIndex,
                            selfNodeIndex,
                            depLabel,
                            insertedWord]

        for o in operationList:
            if o in insertingAction:
                args = argsDic[o][:2]
                args.append(argsDic[o][3])
            elif o in changeRelation:
                args = argsDic[o][1]
                args.append(argsDic[o][2])
            elif o in moveSubtree:
                args = argsDic[o][:2]
            elif o in multiWord:
                args = argsDic[o][1]
            else:
                args = argsDic[o]

            # kList is [[value, ope, args, text, hypo],[]]
            # return of getValue is k best of the operation
            kList.append(o.getValue(text, hypothesis, args))

        # kBest is [[value, ope, args, text, hypo],[]]
        for o in kList:
            # cand is [value, ope, args, text, hypo]
            # return of search2 is k best of o
            cand = search2(o)
            if len(kBest) == 4:
                # compare values
                if cand[0] > kBest[3][0]:
                    kBest[3] = cand
            else:
                kBest.append()
            kBest.sorted(key=lambda x: x[0], reverse=True)

        self.proof.append(kBest)
        self.__feature = self.__getFeature()

    def translate(self):
        if len(self.proof) == 0:
            raise Exception("proofがないです")
        for items in self.proof:
            oper = items[0]
            args = items[1]
            oper.translateT_H(self, args)
