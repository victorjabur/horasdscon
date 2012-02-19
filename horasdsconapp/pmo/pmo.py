#! /usr/bin/python
# coding: utf-8

import requests, re, sys
from unicodedata import normalize

class Pmo:

    def login(self, usuario_pmo=None, senha_pmo=None, request=None, type='complete'):
        if usuario_pmo == None:
            usuario_pmo = request.session['usuario_pmo']
            senha_pmo = request.session['senha_pmo']
        post_login = {'login':'login', 'username':usuario_pmo, 'password':senha_pmo, 'login.x':'13', 'login.y':'12'}
        r = requests.post('http://www.dscon.com.br/pmo/index.php', post_login)
        if type == 'complete:':
            pagina = requests.get('http://dscon.com.br/pmo/index.php?m=projects&tab=1', cookies=r.cookies)
            if pagina.content.find('Usu&aacute;rio e/ou senha inv&aacute;lidos.') != -1:
                raise RuntimeError('Usuario ou Senha Invalidos')
            return LoginInfo(r.cookies, pagina)
        else:
            return r.cookies

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

    def extrairEmpresasFromPagina(self, pagina):
        lista_empresas = []
        empresas = re.findall(r'<option value=.company..*</option>', pagina)
        for empresa in empresas:
            lista_empresas.append(re.search(r"bold...(.*)</option>", empresa).group(1))
        return lista_empresas

    def extrairProjetosFromPagina(self, pagina):
        lista_projetos = []
        projetos = re.findall(r"<td width=.30%.>\n.*\n</td>.*\n.*\n.*", pagina)
        for projeto in projetos:
            empresa = re.search(r"<td width..30..>\n\t(.*)\n</td>", projeto).group(1)
            projectid = re.search(r"project_id.(\d*)..onmou", projeto).group(1)
            projectname = re.search(r"eout=.nd.....(.*)</a>", projeto).group(1)
            print empresa, projectid, " ", projectname

    def retirar_acento(self, str):
        return normalize('NFKD', str.decode('utf-8')).encode('ASCII','ignore')

    def obter_projetos(self,request):
        cookie = self.login(request=request, type='cookie')
        post_projetos = {'department':'company_0'}
        r = requests.post('http://dscon.com.br/pmo/index.php?m=projects', post_projetos, cookies=cookie)
        pagina = r.content
        lista_empresas = self.extrairEmpresasFromPagina(pagina)
        lista_projetos = self.extrairProjetosFromPagina(pagina)


class LoginInfo:
    def __init__(self, cookies, pagina):
        self.cookies = cookies
        self.pagina = pagina

class Colaborador:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

class Projeto:
    def __init__(self, company, projectid, projectcode, projectname, projecttype, taskid, taskname):
        self.company = company
        self.projectid = projectid
        self.projectcode = projectcode
        self.projectname = projectname
        self.projecttype = projecttype
        self.taskid = taskid
        self.taskname = taskname
