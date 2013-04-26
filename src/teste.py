#-*- coding: utf-8 -*-
'''
Created on 20/04/2013

@author: Abel Corrêa
'''
from itertools import izip
from classifier.crossvalidator.KFoldCrossValidator import KFoldCrossValidator
from classifier.bayes.NaiveBayes import NaiveBayes 
if __name__ == '__main__':
    pass
    cv = KFoldCrossValidator(5)
    
    cv.__divideInstances__()
    print cv.kFoldInstances[3]
    a = []
    a