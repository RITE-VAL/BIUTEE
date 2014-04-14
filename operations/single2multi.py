#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operation import *

class Single2Multi(Operation):

    @classmethod
    def getValue(cls, t, h, args=None):
        return -1

    @classmethod
    def transFormTree(cls, h, args=None):
        h[0].flip_part_of_speech()
    
    @classmethod
    def transFormT_H(cls, t_h, args=None):
        t_h.hs.append( [t_h.hs[len(t_h.hs) - 1][0].flip_part_of_speech(),] )