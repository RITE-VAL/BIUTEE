#!/usr/bin/env python
# -*- coding: utf-8 -*-

import trees.pasparser
import sys, os
import ConfigParser
inifile = ConfigParser.SafeConfigParser()
iniPath = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "./config.ini"))
inifile.read(iniPath)
sys.path.append( unicode(inifile.get(u"path", u"LivSVM_PATH")) )
modelPath = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "./models/model"))
from svm import *
from svmutil import *
import collections
from t_h import *

class ML:
    def __parseData(self, dataPath):
        data = []
        for line in open(dataPath):
            line = line.replace("\n", "")
            items = line.split("\t")
            if len(items) != 3:
                continue
            label = items[0]
            t = items[1]
            h = items[2]
            if label == "" or t == "" or h == "":
                continue
            t_h = T_H(t, h, label)
            data.append(t_h)
        return data

    def __getWeight(self, modelPath):
        f = open(modelPath)
        for line in f:
            line = line.replace("\n", "")
            if line.split(" ")[0] == "rho":
                b = float(line.split(" ")[1])
            if line == 'SV':
                break
    
        weight = collections.defaultdict(lambda: 0)
    
        for line in f:
            line = line.replace("\n", "")
            split = line.split(" ")
            coef = float(split[0])
            for feature in split[1:]:
                if feature == " " or feature == "":
                    continue
                number, value = feature.split(':')
                number = int(number)
                value = float(value)
                weight[number] += coef * value
        return [[ weight[num] for num in sorted(weight.keys()) ], b]
    
    
    def train(self, dataPath, w, b, k):
        trainData = self.__parseData(dataPath)
        while(True):
            features = []
            labels = []
            for data in trainData:
                data.search(w, b, k)
                if data.feature == None:
                    print "featureない"
                    continue
                features.append(data.feature)
                labels.append(data.label)
            problem = svm_problem(labels, features)
            parameter = svm_parameter('-s 0 -t 0')
            svm_save_model(modelPath, svm_train(problem, parameter))
            w, b = self.__getWeight(modelPath)
            print "weight %f b %f \n" %(w, b)
            break
        return [w, b]


#filePath = sys.argv[1]
#trainData = []
#for line in open(filePath):
#    items = line.split('\t')
#    if len(items) != 3:
#        continue
#    label = items[0]
#    t = items[1]
#    h = items[2]
#    trainData.append(T_H("", ""))
