#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import requests, re, sys
from unicodedata import normalize

class Pmo:
    def login(self, usuario, senha):
        post_login = {'login':'login', 'username':usuario, 'password':senha, 'login.x':'13', 'login.y':'12'}
        r = requests.post('http://www.dscon.com.br/pmo/index.php', post_login)
        pagina = requests.get('http://dscon.com.br/pmo/index.php?m=projects&tab=1', cookies=r.cookies)
        if pagina.content.find('Usu&aacute;rio e/ou senha inv&aacute;lidos.') != -1:
            raise RuntimeError('Usuario ou Senha Invalidos')
        return LoginInfo(r.cookies, pagina)

    def extrairColaboradorFromPagina(self, pagina):
        pagina = self.retirar_acento(pagina.content)
        nome_colaborador = re.search(r'Bem-vindo (.*)</td>', pagina).group(1)
        nomes_bem_vindo = nome_colaborador.split(' ')
        colaboradores = re.findall(r"<OPTION VALUE='\d*'>[\w()\s,-\.]*", pagina)
        id_colaborador = ''
        for colaborador in colaboradores:
            colaborador = colaborador.replace(',','').strip()
            colaborador = re.sub(r'\(.*\)', '', colaborador)
            colaborador = colaborador.strip()
            nomes_colaborador = re.search(r'<OPTION VALUE=.\d*.>(.*)', colaborador).group(1)
            nomes_colaborador = nomes_colaborador.split(' ')
            intersecao = set(nomes_bem_vindo).intersection(set(nomes_colaborador))
            if len(intersecao) == len(nomes_bem_vindo) == len(nomes_colaborador):
                id_colaborador = re.search(r'<OPTION VALUE=.(\d*).>', colaborador).group(1)
        return Colaborador(id_colaborador, nome_colaborador)

    def retirar_acento(self, str):
        return normalize('NFKD', str.decode('iso-8859-1')).encode('ASCII','ignore')


class LoginInfo:
    def __init__(self, cookies, pagina):
        self.cookies = cookies
        self.pagina = pagina

class Colaborador:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome