#! /usr/bin/python
# coding: utf-8

import requests, re, sys
from unicodedata import normalize
from horasdsconapp.Util import Util

class Pmo:

    def __init__(self):
        self.util = Util()

    def login(self, usuario_pmo=None, senha_pmo=None, request=None, type='complete'):
        if usuario_pmo == None:
            usuario_pmo = request.session['usuario_pmo']
            senha_pmo = request.session['senha_pmo']
        post_login = {'login':'login', 'username':usuario_pmo, 'password':senha_pmo, 'login.x':'13', 'login.y':'12'}
        r = requests.post('http://www.dscon.com.br/pmo/index.php', post_login)
        if type == 'complete':
            pagina = requests.get('http://dscon.com.br/pmo/index.php?m=projects&tab=1', cookies=r.cookies)
            if pagina.content.find('Usu&aacute;rio e/ou senha inv&aacute;lidos.') != -1:
                raise RuntimeError('Usuario ou Senha Invalidos')
            return LoginInfo(r.cookies, pagina)
        else:
            return r.cookies

    def extrairColaboradorFromPagina(self, pagina):
        pagina = self.util.retirar_acento(pagina.content)
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
        for i,empresa in enumerate(empresas):
            nome_empresa = re.search(r"bold...(.*)</option>", empresa).group(1)
            lista_empresas.append(Empresa(i, nome_empresa))
        return lista_empresas

    def extrairProjetosFromPagina(self, pagina):
        lista_projetos = []
        projetos = re.findall(r"<td width=.30%.>\n.*\n</td>.*\n.*\n.*", pagina)
        for projeto in projetos:
            nome_empresa = re.search(r"<td width..30..>\n\t(.*)\n</td>", projeto).group(1)
            id_projeto = re.search(r"project_id.(\d*)..onmou", projeto).group(1)
            nome_projeto = re.search(r"eout=.nd.....(.*)</a>", projeto).group(1)
            lista_projetos.append(Projeto(company_id=self.getEmpresa_id_from_nome(nome_empresa, self.lista_empresas), projectid=id_projeto, projectname=nome_projeto))
        return lista_projetos

    def extrairTarefasFromIdProjeto(self, request, idProjeto):
        lista_tarefas = []
        cookie = self.login(request=request, type='cookie')
        pagina = requests.get('http://dscon.com.br/pmo/index.php?m=projects&a=view&project_id=' + str(idProjeto), cookies=cookie).content
        acabou = False
        while acabou == False:
            tarefas = re.findall(r"&project_id=\d*&open_task_id=\d*\"><img", pagina)
            if len(tarefas) > 0:
                tarefa = tarefas.pop()
                id_projeto = re.search(r"&project_id=(\d*)&op", tarefa).group(1)
                open_task_id = re.search(r"&open_task_id=(\d*)\"><img", tarefa).group(1)
                pagina = requests.get('http://dscon.com.br/pmo/index.php?m=projects&a=view&project_id=' + id_projeto + '&open_task_id=' + open_task_id, cookies=cookie).content
            else:
                acabou = True
        tarefas = re.findall(r"\">&nbsp;<a href=../index.php.m=tasks&a=view&task_id=.*", pagina)
        for tarefa in tarefas:
            id_tarefa = re.search(r"task_id.(\d*).log", tarefa).group(1)
            nome_tarefa = re.search(r"#log\"  >([^<]*)", tarefa).group(1)
            lista_tarefas.append(Tarefa(id_tarefa, nome_tarefa))
        tarefas = re.findall(r"expand.gif\" border=\"0\" /></a>&nbsp;<a href=../index.php.m=tasks&a=view&task_id=.*", pagina)
        for tarefa in tarefas:
            id_tarefa = re.search(r"task_id.(\d*).log", tarefa).group(1)
            nome_tarefa = re.search(r"<b><i>(.*)</i></b>", tarefa).group(1)
            lista_tarefas.append(Tarefa(id_tarefa, nome_tarefa))
        return lista_tarefas

    def obter_projetos(self,request):
        cookie = self.login(request=request, type='cookie')
        post_projetos = {'department':'company_0'}
        r = requests.post('http://dscon.com.br/pmo/index.php?m=projects', post_projetos, cookies=cookie)
        pagina = r.content
        self.lista_empresas = self.extrairEmpresasFromPagina(pagina)
        self.lista_projetos = self.extrairProjetosFromPagina(pagina)

    def getEmpresa_id_from_nome(self, nome_empresa, lista_empresas):
        for empresa in lista_empresas:
            if self.util.is_string_equals_ignorecase(empresa.company_name, nome_empresa):
                return empresa.company_id
        return None


class LoginInfo:
    def __init__(self, cookies, pagina):
        self.cookies = cookies
        self.pagina = pagina

class Colaborador:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

class Empresa:
    def __init__(self, company_id='', company_name=''):
        self.company_id = company_id
        self.company_name = company_name

class Tarefa:
    def __init__(self, id_tarefa='', nome_tarefa=''):
        self.id_tarefa = id_tarefa
        self.nome_tarefa = nome_tarefa

class Projeto:
    def __init__(self, company_id='', projectid='', projectcode='', projectname='', projecttype='', taskid='', taskname=''):
        self.company_id = company_id
        self.projectid = projectid
        self.projectcode = projectcode
        self.projectname = projectname
        self.projecttype = projecttype
        self.taskid = taskid
        self.taskname = taskname
