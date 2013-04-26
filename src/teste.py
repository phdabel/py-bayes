#-*- coding: utf-8 -*-
'''
Created on 20/04/2013

@author: Abel Corrêa
'''
from itertools import izip

from classifier.bayes.NaiveBayes import NaiveBayes 
if __name__ == '__main__':
    pass
    nb = NaiveBayes()
    a = (nb.labelClassifier())
    print a