#! /usr/bin/python
# coding: utf-8

import os, sys, re
from ConfigParser import RawConfigParser
from unicodedata import normalize

class Util:

    def __init__(self):
        self.PYTHON_CONF = ''

    def setConfigurationFile(self, PYTHON_CONF):
        self.PYTHON_CONF = PYTHON_CONF

    def getConfigurationFile(self):
        config = RawConfigParser()
        config.read(self.PYTHON_CONF)
        return config

    def getEntry(self, setor, chave):
        config = self.getConfigurationFile()
        conf = config.get(setor, chave)
        conf = conf.replace('RAIZ_LOCAL', config.get('geral', 'RAIZ_LOCAL'))
        conf = conf.replace('RAIZ_REMOTA', config.get('geral', 'RAIZ_REMOTA'))
        return conf

    def pathJoin(self, raiz, diretorio):
        return os.path.join(raiz, diretorio).replace('\\', '/')

    def is_string_equals_ignorecase(self, str1, str2):
        if (unicode(str1,'utf-8').lower()).find(unicode(str2,'utf-8').lower()) == -1:
            return False
        else:
            return True

    def retirar_acento(self, str):
        return normalize('NFKD', str.decode(sys.getfilesystemencoding())).encode('ASCII','ignore')

