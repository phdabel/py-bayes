#-*- coding: utf-8 -*-
'''
Created on 20/04/2013

@author: Abel Corrêa
'''
from classifier.crossvalidator.KFoldCrossValidator import KFoldCrossValidator
from classifier.bayes.NaiveBayes import NaiveBayes 
if __name__ == '__main__':
    pass
    cv = KFoldCrossValidator(10)
    nb = NaiveBayes()
    
    cv.kFoldCrossValidate()
    