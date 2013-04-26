#-*- coding: utf-8 -*-
'''
Created on 20/04/2013

@author: Abel Corrêa
'''
from fileAssembler.FileAssembler import FileAssembler

class KFoldCrossValidator(object):
    '''
    K-Fold CrossValidation
    Deve ser setado o valor de k, com base nisso o classificador particionara
    as amostras em proporção igual para as classes existentes no arquivo.
    k: valor k para cross fold, por padrao k = 10
    instanciasByClass: dicionario das instancias dividias pelas classes
            para facilitar o crossValidation
    instancias: array contendo todas as instancias de acordo com o arquivo nbf
    '''
    
    k = 0
    instanciasByClass = {}
    instancias = []
    kFoldInstances = []

    def __init__(self, k=10):
        '''
        Constructor
        '''
        self.setK(k)
        self.kFoldInstances = [[]]*k
        self.__defineInstances__()
    
    '''
    Ajusta o valor de k, por padrao 10
    '''
    def setK(self, k=10):
        self.k = k
    
    '''
        Metodo privado da classe
        define as instancias contidas no arquivo para a variavel instancias da Classe NayveBayes.
    '''    
    def __defineInstances__(self):
        for line in FileAssembler.readDataFile(FileAssembler).readlines():
            self.instancias.append(eval(line))
        tmp = ""
        ct = 0
        for i in self.instancias:
            if(i[1][0]!=tmp):
                tmp = i[1][0]
                self.instanciasByClass[tmp] = {}
            self.instanciasByClass[tmp][str(ct)] = i[0]
            ct = ct +1
    
    '''
    Metodo para separar as instancias e guarda-las na variavel kFoldInstances
    A variavel e dividida da seguinte maneira
    kFoldInstances = [
    [instancia1]
    [instancia2]
    [instancia3]
    ...
    [instanciaK]
    ]
    E cada k array e composto das n tuplas [[atributos][classe]] 
    divididas proporcionalmente conforme o tamanho do arquivo de amostras
    
    a instancias 1 ate k-1 sao utilizadas para treino do classificador
    a instancia k e utilizada para teste 
    '''
    def __divideInstances__(self):
        length = []
        for c in self.instanciasByClass:
            length.append(float(len(self.instanciasByClass[c]))/self.k)
        for ktmp in range(0,self.k):
            countRemove = 0
            countClass = 0
            for c in self.instanciasByClass:
                while countRemove < length[countClass]:
                    self.kFoldInstances[ktmp].append([self.instanciasByClass[c].popitem()[1],[str(c)]])
                    countRemove = countRemove + 1
                countClass = countClass + 1
                countRemove = 0