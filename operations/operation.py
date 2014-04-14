#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

class Operation:
    __metaclass__ = ABCMeta

    @classmethod
    @abstractmethod
    def getValue(cls, t, h, w, b, arg=None):return

    @classmethod
    @abstractmethod
    def getKBest(cls, t, h, args, w, b, k):return

    @classmethod
    @abstractmethod
    def transFormTree(cls, h, arg=None):pass

    @classmethod
    @abstractmethod
    def transFormT_H(cls, t_h, arg=None):pass
