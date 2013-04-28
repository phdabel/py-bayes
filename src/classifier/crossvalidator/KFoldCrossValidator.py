#-*- coding: utf-8 -*-
'''
Created on 20/04/2013

@author: Abel Corrêa
'''
from fileAssembler.FileAssembler import FileAssembler
from classifier.bayes.NaiveBayes import NaiveBayes

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
        for i in range(0, self.k):
            self.kFoldInstances.append([])
        self.__defineInstances__()
        self.__divideInstances__()
    
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
        '''
            essa parte calcula quantas amostras cada k-fold deve possuir
            e monta variaveis de apoio
        '''
        length = []
        count = []
        for i in range(0, self.k):
            count.append(0)
        ktmp = 0
        '''
           calculo do numero de amostras, proporcao por k-fold 
        '''
        for c in self.instanciasByClass:
            count.append(0)
            length.append(float(len(self.instanciasByClass[c]))/self.k)
        countClass = 0
        '''
            montagem das amostras em cada k-fold
        '''
        for c in self.instanciasByClass:
            for i in self.instanciasByClass[c]:
                if count[countClass] < length[countClass]:
                    self.kFoldInstances[ktmp].append([self.instanciasByClass[c][i],[str(c)]])
                    #print "fold %d, classe - %s, amostra - %s"%(ktmp,c,self.instanciasByClass[c][i])
                    count[countClass] = count[countClass] + 1
                else:
                    ktmp = ktmp + 1
                    count[countClass] = 0
            ktmp = 0
            countClass = countClass + 1
    
    '''
        Montar Matriz de Confusao
    '''
    def __confusionMatrix__(self, instanciaTreino, instanciaTeste):
        nbTreino = NaiveBayes(instanciaTreino)
        nbTeste = NaiveBayes(instanciaTeste)
        testClass = ''
        trainClass = ''
        vp = 0
        vn = 0
        fp = 0
        fn = 0
        rotulo = nbTreino.labelClassifier()
        for a in nbTeste.vocabularySize:
            if nbTeste.probClassGivenAttribute(rotulo, a) > 0.5 and nbTreino.probClassGivenAttribute(rotulo, a) > 0.5:
                vp = vp + 1
            elif nbTeste.probClassGivenAttribute(rotulo, a) <= 0.5 and nbTreino.probClassGivenAttribute(rotulo, a) > 0.5:
                fp = fp + 1
            elif nbTeste.probClassGivenAttribute(rotulo, a) > 0.5 and nbTreino.probClassGivenAttribute(rotulo, a) <= 0.5:
                fn = fn +1
            else:
                vn = vn +1
        print "______________"
        print "---- P---N----"
        print "P---%d---%d---"%(vp,fn)
        print "N---%d---%d---"%(fp,vn)

        
    '''
    efetua validacao dos dados
    e monta k matrizes de confusao
    '''
    def kFoldCrossValidate(self):
        instanciaTreino = []
        instanciaTeste = []
        ct = 0
        for cv in range(0,self.k):
            for k in self.kFoldInstances:
                for i in k:
                    if cv != ct:
                        #print "k - %d, i - %s"%(cv,i)
                        instanciaTreino.append(i)
                    else:
                        instanciaTeste.append(i)
                ct = ct + 1
            ct = 0
            print "Matriz de Confusão do Modelo "+str(cv + 1)
            self.__confusionMatrix__(instanciaTreino, instanciaTeste)
            instanciaTreino = []
            instanciaTeste = []