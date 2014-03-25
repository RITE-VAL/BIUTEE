#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

class Operation:
    __metaclass__ = ABCMeta

    @classmethod
    @abstractmethod
    def getValue(cls, t, h, args):return

    @classmethod
    @abstractmethod
    def translateTree(cls, h, args):pass

    @classmethod
    @abstractmethod
    def translateT_H(cls, t_h, args):pass
