#-*- coding: utf-8 -*-
'''
Created on 20/04/2013

@author: Abel Correa
'''
import sys, os
import codecs
from fileAssembler.constants import *

class FileAssembler(object):
    '''
    classdocs
    '''
    
    
    def __init__(self):
        '''
        Constructor
        '''
    
    '''
        Metodo Estatico para percorrer um arquivo texto e trata-lo retirando pontuacao e outros caracteres especiais.
        Retorna uma instancia para uso no classificador dentro do padrao:
        ['atributo1' 'atributo2' 'atributo3']['classe']
    '''
    @staticmethod
    def readClassFiles(self, nomeArquivo, classe):
        file = ""
        try:
            file = codecs.open(nomeArquivo, "r", 'utf-8')
            linha = file.read()
            linha = self.__replaceAll__(self, linha).replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ")
            linha = linha.split(" ")
            instancia = "["
            for c in linha:
                instancia = instancia + " \""+c+"\","
            instancia = instancia + " ],[\""+classe+"\"]"
        except:
            instancia = 'Arquivo invalido'
        return instancia
    
    '''
        Metodo Estatico para substituir os caracteres especiais do texto por espaco em branco.
        Caracteres especiais sao definidos na variavel global
    '''
    @staticmethod
    def __replaceAll__(self, text):
        for c in SPECIALCHAR:
            text = text.replace(c," ")
        return text.lower()
    
    '''
        Metodo para gravar um arquivo de dados data.nbf (nayve bayes file) com uma amostra passada como parametro.
    '''
    @staticmethod
    def writeDataFile(self, data):
        file = ""
        try:
            file = codecs.open(DATA_DIR+'data.nbf', "a", 'utf-8')
            file.write(data+"\n")
            file.close()
        except:
            return "Erro ao gravar arquivo nbf!"
        
    '''
        Metodo Estatico para retornar o arquivo de dados em uma variavel.
    '''
    @staticmethod
    def readDataFile(self):
        file = ""
        try:
            file = codecs.open(DATA_DIR+'data.nbf', "r", 'utf-8')
        except:
            file = 'Arquivo invalido'
        return file