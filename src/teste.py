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
    #print cv.instanciasByClass['positivo']
    
    cv.__divideInstances__()
    '''
    print cv.kFoldInstances

    cv.kFoldInstances[0].append([['teste'],['classe']])
    cv.kFoldInstances[0].append([['teste2'],['classe']])
    cv.kFoldInstances[0].append([['teste3'],['classe']])
    print "fold: %s"%cv.kFoldInstances
    print cv.kFoldInstances[0]
    print cv.kFoldInstances[1]
    '''
    print len(cv.kFoldInstances[0])
    for i in cv.kFoldInstances[0]:
        print i