#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import os
from ConfigParser import RawConfigParser

class Util:

    def __init__(self):
        self.PYTHON_CONF = ''

    def setConfigurationFile(self, PYTHON_CONF):
        self.PYTHON_CONF = PYTHON_CONF

    def getConfigurationFile(self, caminhoArquivoConfiguracao):
        config = RawConfigParser()
        config.read(self.PYTHON_CONF)
        return config

    def getEntry(self, setor, chave):
        config = self.getConfigurationFile(self.PYTHON_CONF)
        conf = config.get(setor, chave)
        conf = conf.replace('RAIZ_LOCAL', config.get('geral', 'RAIZ_LOCAL'))
        conf = conf.replace('RAIZ_REMOTA', config.get('geral', 'RAIZ_REMOTA'))
        return conf

    def pathJoin(self, raiz, diretorio):
        return os.path.join(raiz, diretorio).replace('\\', '/')
