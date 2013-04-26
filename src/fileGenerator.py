#-*- coding: utf-8 -*-
'''
Created on 20/04/2013

@author: Abel Corrêa
'''
from fileAssembler.FileAssembler import FileAssembler
from fileAssembler.constants import *

if __name__ == '__main__':
    pass
    #diretorio pode ser POSITIVE_DIR ou NEGATIVE_DIR
    for p in range(0,450):
        arquivo = POSITIVE_DIR +str(p)+".txt"
        data = FileAssembler.readClassFiles(FileAssembler, arquivo, 'positivo')
        FileAssembler.writeDataFile(FileAssembler, data)
    for n in range(0,230):
        arquivo = NEGATIVE_DIR +str(n)+".txt"
        data = FileAssembler.readClassFiles(FileAssembler, arquivo, 'negativo')
        FileAssembler.writeDataFile(FileAssembler, data)
    print 'Arquivo data.nbf gerado com as instâncias.'