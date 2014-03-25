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
        wordList = ["word", "word2"]
        fposDic = {}
        fposDic["insertPos"] = 1
        fposDic["inserWord"] = wordList[0]
        argsDic[FlipPos] = [fposDic]
        for o in operationList:
            args = argsDic[o]
            value = o.getValue(text, hypothes, args)
            
            # argsをいい感じに変形させていって全部試す(forなりなんなり使ってください)
            if "insertNum" in args:
                args["insertNum"] = wordList[1]
            if "insertNum" in args:
                args["insertPos"] += 1
            value = FlipPos.getValue(text, hypothes, args)
            o.translateTree(hypothes, args) # 変形させてまた次の操作を探す
        
        self.proof.append([FlipPos, args])
        
        
        self.__feature = self.__getFeature()

    def translate(self):
        if len(self.proof) == 0:
            raise Exception("proofがないです")
        for items in self.proof:
            oper = items[0]
            args = items[1]
            oper.translateT_H(self, args)
