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
            length.append(float((len(self.instanciasByClass[c]))/self.k) - 1)
        countClass = 0
        '''
            montagem das amostras em cada k-fold
        '''
        for c in self.instanciasByClass:
            for i in self.instanciasByClass[c]:
                if count[countClass] < int(length[countClass]):
                    #print "contaClass %d"%(count[countClass])
                    #print "class %s - kfold %d, %d < %d "%(str(c),ktmp,count[countClass],int(length[countClass]))
                    self.kFoldInstances[ktmp].append([self.instanciasByClass[c][i],[str(c)]])
                    count[countClass] = count[countClass] + 1
                else:
                    self.kFoldInstances[ktmp].append([self.instanciasByClass[c][i],[str(c)]])
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
        rotulo = 'positivo'#nbTreino.labelClassifier()
        #for a in nbTeste.instancias:
        #    print nbTeste.probGivenInstance(a[0])
        
        for a in nbTeste.instancias:
            probTeste = a[1][0]
            probTreino = nbTreino.probGivenInstance(a[0])
            if (probTeste == rotulo and probTreino == rotulo):
                vp = vp + 1
            elif (probTeste != rotulo and probTreino != rotulo):
                vn = vn + 1
            elif (probTeste == rotulo and probTreino != rotulo):
                fp = fp + 1
            elif (probTeste != rotulo and probTreino == rotulo):
                fn = fn + 1
        print "  ______________"
        print " |    P    N    "
        print "P|    %d    %d    "%(vp,fn)
        print "N|    %d    %d    "%(fp,vn)
        print "  TTTTTTTTTTTTTT "
        return [vp, vn, fp, fn]

    '''
    efetua validacao dos dados
    e monta k matrizes de confusao
    '''
    def kFoldCrossValidate(self):
        instanciaTreino = []
        instanciaTeste = []
        matrixValue = []
        avgMatrix = [0,0,0,0]
        ct = 0
        for cv in range(0,self.k):
            for kFold in self.kFoldInstances:
                for i in kFold:
                    if cv != ct:
                        instanciaTreino.append(i)
                    else:
                        instanciaTeste.append(i)
                ct = ct + 1
            ct = 0
            print "Matriz de Confusão do Modelo "+str(cv + 1)
            matrixValue.append(self.__confusionMatrix__(instanciaTreino, instanciaTeste))
            avgMatrix[0] = avgMatrix[0] + matrixValue[cv][0]
            avgMatrix[1] = avgMatrix[1] + matrixValue[cv][1]
            avgMatrix[2] = avgMatrix[2] + matrixValue[cv][2]
            avgMatrix[3] = avgMatrix[3] + matrixValue[cv][3]
            instanciaTreino = []
            instanciaTeste = []
        avgMatrix[0] = float(avgMatrix[0]) / float(self.k)
        avgMatrix[1] = float(avgMatrix[1]) / float(self.k)
        avgMatrix[2] = float(avgMatrix[2]) / float(self.k)
        avgMatrix[3] = float(avgMatrix[3]) / float(self.k)
        vp = avgMatrix[0]
        vn = avgMatrix[1]
        fp = avgMatrix[2]
        fn = avgMatrix[3]
        devMatrix = [0.0,0.0,0.0,0.0]
        for k in matrixValue:
            devMatrix[0] = pow((k[0] - avgMatrix[0]),2)
            devMatrix[1] = pow((k[1] - avgMatrix[1]),2)
            devMatrix[2] = pow((k[2] - avgMatrix[2]),2)
            devMatrix[3] = pow((k[3] - avgMatrix[3]),2)
        devMatrix[0] = devMatrix[0] / float((self.k - 1))
        devMatrix[1] = devMatrix[1] / float((self.k - 1))
        devMatrix[2] = devMatrix[2] / float((self.k - 1))
        devMatrix[3] = devMatrix[3] / float((self.k - 1)) 
        print "Matriz de Confusao media"
        print "  ____________________"
        print " |       P       N    "
        print "P|      %.1f    %.1f    "%(vp,fn)
        print "N|      %.1f    %.1f    "%(fp,vn)
        print "  TTTTTTTTTTTTTTTTTTT "
        print "Desvio Padrao"
        print "dvp - %.2f"%(devMatrix[0])
        print "dvn - %.2f"%(devMatrix[1])
        print "dfp - %.2f"%(devMatrix[2])
        print "dfn - %.2f"%(devMatrix[3])
        p = vp / (vp + fp)
        print "Precisao - %.2f"%(p)
        tvp = vp / (vp + fn)
        print "TVP - %.2f"%(tvp)
        tfp = fp / (fp + vn)
        print "TFP - %.2f"%(tfp)
        #tvn = vn / (fp + vn)
        #print "TVN - %.2f"%(tvn)
        f = (2*p*tvp) / (p+tvp)
        print "Medida - F = %.2f"%(f)