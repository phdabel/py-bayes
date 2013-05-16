#-*- coding: utf-8 -*-
'''
Created on 20/04/2013

@author: Abel Corrêa
'''
from fileAssembler.FileAssembler import FileAssembler
from classifier.bayes.constants import *
from decimal import Decimal
import math

class NaiveBayes(object):
    '''
        instancias: array contendo todas as instancias de acordo com o arquivo nbf
        classes: dicionario contendo todas as classes existentes no arquivo nbf
            com os totais (total) e a probabilidade a priori delas (prob) = p(v)
        totalInstances: total de instancias
        attributes: probabilidades dos atributos dada classe p(a|v)
        attributesSize: dicionario contendo o total de atributos para cada classe
        labelNB: rotulo de classificacao vNB
        vocabularySize: total de atributos nao repetidos em ambas as classes
        estimator: define um estimador para o calculo da probabilidade default None
    '''
    instancias = []
    classes = {}
    totalInstances = 0
    attributes = {}
    labelNB = {}
    vocabularySize = {}
    estimator = None
    
    
    def __init__(self, instancias=None):
        self.__defineInstances__(instancias)
        self.__classProbability__()
        self.__attributesProbability__()
        self.__getAttributes__()
        
    '''
        Metodo privado da classe
        define as instancias contidas no arquivo para a variavel instancias da Classe NayveBayes.
    '''    
    def __defineInstances__(self, instancias=None):
        if(instancias == None):
            for line in FileAssembler.readDataFile(FileAssembler).readlines():
                self.instancias.append(eval(line))
        else:
            self.instancias = instancias

    '''
        define as probabilidades das classes e armazena no vetor classes
        prob(v) -> self.classes[v]['prob']
        total de v-> self.classes[v]['total']
    '''
    def __classProbability__(self):
        tmp=""
        for i in self.instancias:
            if(i[1][0]!=tmp):
                tmp = i[1][0]
                self.classes[tmp] = {}
            if(self.classes[tmp].has_key('prob')):
                self.classes[tmp]['prob'] = self.classes[tmp]['prob'] + 1
                self.classes[tmp]['total'] = self.classes[tmp]['total'] + 1
            else:
                self.classes[tmp]['prob'] = 1
                self.classes[tmp]['total'] = 1
            self.totalInstances = self.totalInstances + 1
        for i in self.classes:
            self.classes[i]['prob'] = float(self.classes[i]['prob'])/float(self.totalInstances)
        
    
    '''
        define os atributos independentes de cada classe
        p(a|v) = self.attributes[v][a]['prob']
        total de a em v = self.attributes[v][a]['total']
    '''
    def __attributesProbability__(self):
        tmp=""
        for i in self.instancias:
            if(i[1][0]!=tmp):
                tmp = i[1][0]
                self.attributes[tmp] = {}
            for a in i[0]:
                if not self.attributes[tmp].has_key(a):
                    self.attributes[tmp][a] = {'prob':1.0, 'total':1}
                elif self.attributes[tmp].has_key(a) and (a != '' or a!=' '):
                    self.attributes[tmp][a]['prob'] = self.attributes[tmp][a]['prob'] + 1.0
                    self.attributes[tmp][a]['total'] = self.attributes[tmp][a]['total'] + 1
        for givenClass in self.attributes:
            for attributes in self.attributes[givenClass]:
                self.attributes[givenClass][attributes]['prob'] = float(self.attributes[givenClass][attributes]['prob'])/float(self.classes[givenClass]['total'])
    
    '''
        Define o numero de atributos para ambas as classes sem repeticao
    '''
    def __getAttributes__(self):
        for c in self.attributes:
            for a in self.attributes[c]:
                if a!='' and not self.vocabularySize.has_key(a):
                    self.vocabularySize[a] = self.attributes[c][a]['total']
                elif a!= '':
                    self.vocabularySize[a] = self.vocabularySize[a] + self.attributes[c][a]['total']

    
    '''
        Calcula o rotulo de classificacao das instancias
        retorna o indice mais alto do dicionario labelNB (rotulo NaiveBayes)
    '''
    def labelClassifier(self):
        if self.labelNB == {}:
            for classes in self.attributes:
                if not self.labelNB.has_key(classes):
                    self.labelNB[classes] = (0.0)
                for attributes in self.attributes[classes]:
                    self.labelNB[classes] = self.labelNB[classes] + (math.log(self.probWithEstimator(attributes, classes)))
                self.labelNB[classes] = self.labelNB[classes] * (math.log(self.classes[classes]['prob']))
        
        return ARGMAX(self.labelNB)
                    
    '''
        Define um estimador para o calculo da probabilidade
        estimator pode ser: laplacian ou none
    '''
    def setEstimator(self, estimator):
        self.estimator = estimator
        
    '''
        retorna a probabilidade de um atributo dado uma classe
    '''
    def probWithEstimator(self, someAttribute, someClass):
        if self.attributes[someClass].has_key(someAttribute):
            nkj = self.attributes[someClass][someAttribute]['total']
        else:
            nkj = 0
        nj = self.classes[someClass]['total']
        m = len(self.vocabularySize)
        return ((nkj)+(1.0))/(nj+m)
        #return ((nkj)+(((1.0)/len(self.attributes[someClass]))*m))/((nj)+(m))
    
    
    '''
        probabilidade de uma classe dada uma instancia inteira
    '''
    def probClassGivenInstance(self, someClass, someInstance):
        num = 1.0
        pAtrAp = 1.0
        for instanceAttribute in someInstance:
            #instanceAttribute = someInstance[someClass][i]
            num = num * self.probWithEstimator(instanceAttribute, someClass)
            pAtrAp = pAtrAp * self.probAttribute(instanceAttribute)
        res = 0.0
        res = (num * self.classes[someClass]['prob']) / pAtrAp
        return res
    
    
    '''
        probabilidade de uma classe dado um attributo
    '''
    def probClassGivenAttribute(self, someClass, someAttribute):
        pAtCl = self.probWithEstimator(someAttribute, someClass)
        '''
        probabilidade a priori do attribute
        '''
        pAtPriori = self.probAttribute(someAttribute)
        '''
        probabilidade a priori da classe
        '''
        pClPriori = self.probClass(someClass)
        return float((pAtCl*pClPriori)/pAtPriori)

    '''
    probabilidade do atributo a priori
    '''
    def probAttribute(self, someAttribute):
        pAtPriori = 0.0
        for i in self.classes:
            if self.attributes[i].has_key(someAttribute):
                pAtPriori = pAtPriori + self.attributes[i][someAttribute]['prob']
            else: 
                pAtPriori = pAtPriori + self.probWithEstimator(someAttribute, i)
        return pAtPriori

    '''
    probabilidade da classe a priori
    '''
    def probClass(self, someClass):
        pClPriori = 0.0
        for i in self.classes:
            pClPriori = pClPriori + self.classes[i]['prob']
        return pClPriori