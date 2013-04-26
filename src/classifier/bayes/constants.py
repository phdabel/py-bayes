#-*- coding: utf-8 -*-
'''
Created on 24/04/2013

@author: Abel Corrêa
'''
import os

ARGMAX = lambda dict: [key for key, value in dict.items() if value == max(dict.itervalues())][0]