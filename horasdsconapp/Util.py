#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import os
from ConfigParser import RawConfigParser

class Util:

    def getConfigurationFile(self, caminhoArquivoConfiguracao):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        PYTHON_CONF = os.path.abspath(self.pathJoin(BASE_DIR, caminhoArquivoConfiguracao))
        config = RawConfigParser()
        config.read(PYTHON_CONF)
        return config

    def getEntry(self, setor, chave, caminhoArquivoConfiguracao):
        config = self.getConfigurationFile(caminhoArquivoConfiguracao)
        conf = config.get(setor, chave)
        conf = conf.replace('RAIZ_LOCAL', config.get('geral', 'RAIZ_LOCAL'))
        conf = conf.replace('RAIZ_REMOTA', config.get('geral', 'RAIZ_REMOTA'))
        return conf

    def pathJoin(self, raiz, diretorio):
        return os.path.join(raiz, diretorio).replace('\\', '/')
