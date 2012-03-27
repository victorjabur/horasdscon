#! /usr/bin/python
# coding: utf-8
from django.views.decorators.csrf import csrf_protect
from django.utils import simplejson

from unicodedata import normalize

from django import template

from social_auth.views import complete as social_complete

from django.contrib.auth import logout as auth_logout
from django.contrib.messages.api import get_messages
from django.http import HttpResponseRedirect, HttpResponse

from social_auth import __version__ as version

from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from forms import CriarPlanilha
from horasdsconapp.google.spreadsheet import GoogleSpreadsheet
from horasdsconapp.pmo.pmo import Pmo
from horasdsconapp.user.user import User
import settings, re, sys

register = template.Library()

def handle_error500(request, template_name='error/500.html'):
    return render_to_response(template_name, context_instance=RequestContext(request))


def handle_error404(request, template_name='error/404.html'):
    return render_to_response(template_name, context_instance=RequestContext(request))

def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return HttpResponseRedirect('existeplanilha')
    else:
        return render_to_response('home.html', {'version': version},
            RequestContext(request))

@login_required
def existeplanilha(request):
    request.session.set_expiry(60*60)
    googleSpr = GoogleSpreadsheet(request)
    if googleSpr.planilha_existe():
        ctx = {'version': version,
               'last_login': request.session.get('social_auth_last_login_backend')}
        return HttpResponseRedirect('/projetos')
    else:
        form_criarplanilha = CriarPlanilha()
        ctx = {'nome_planilha_horas': settings.NOME_PLANILHA_HORAS,
               'form': form_criarplanilha,}
        return render_to_response('criarplanilha.html', ctx, context_instance=RequestContext(request))

@login_required
@csrf_protect
def criarplanilha(request):
    if request.method == 'POST':
        form = CriarPlanilha(request.POST)
        if form.is_valid():
            usuario_pmo = form.cleaned_data.get('usuario_pmo')
            senha_pmo = form.cleaned_data.get('senha_pmo')
            gsp = GoogleSpreadsheet(request)
            gsp.criar_planilha(request, usuario_pmo, senha_pmo)
            return HttpResponseRedirect('/projetos')
        else:
            ctx = {'form': form,
            }
            return render_to_response('criarplanilha.html', ctx, context_instance=RequestContext(request))

@login_required
@csrf_protect
def criarprojetos(request):
    pass

@login_required
def ajax_empresas(request):
    return get_json_kendoui(request, request.session['lista_empresas'], {'value':'IdEmpresa','text':'NomeEmpresa'})

def get_json_kendoui(request, lista=[], dictname={'value':'value', 'text':'text'}):
    if lista != None:
        list_items = []
        if '$filter' in request.GET:
            filter = request.GET['$filter']
            filterfunction = re.search(r"(\w*)", filter).group(1)
            stringfilter = re.search(r"'(.*)'", filter).group(1)
            lista = filtra_lista(request, filterfunction, lista, stringfilter)
        for i,f in enumerate(lista):
            dict = {}
            dict[dictname['value']] = f
            dict[dictname['text']] = f
            list_items.append(dict)
        data = simplejson.dumps({'d':{'results':list_items, '__count' : str(len(list_items))}})
    else:
        data = ''
    return HttpResponse(request.GET['$callback'] + '(' + data + ')',mimetype='text/javascript;charset=utf-8')

def filtra_lista(request, funcao, lista, stringfiltro):
    if funcao == 'substringof':
        lista_filtrada = []
        for item in lista:
            if is_string_equals_ignorecase(item, stringfiltro):
                lista_filtrada.append(item)
        return lista_filtrada

def is_string_equals_ignorecase(str1, str2):
    if retirar_acento(str1).lower().find(retirar_acento(str2.lower())) == -1:
        return False
    else:
        return True

def retirar_acento(str):
    return normalize('NFKD', str.decode(sys.getfilesystemencoding())).encode('ASCII','ignore')

@login_required
def ajax_projetos(request):
    option = re.search(r"NomeEmpresa eq '(.*)'", request.GET['$filter']).group(1)
    projetos = []
    option = str(option.encode('utf-8'))
    lista_projetos = request.session['lista_projetos']
    for projeto in lista_projetos:
        if projeto.company == option or option == 'Todos':
            dict = {}
            dict['IdProjeto'] = projeto.projectid
            dict['NomeProjeto'] = projeto.projectname
            projetos.append(dict)
    data = simplejson.dumps({'d':{'results':projetos}})
    return HttpResponse(request.GET['$callback'] + '(' + data + ')',mimetype='text/javascript;charset=utf-8')

@login_required
@csrf_protect
def projetos(request):
    lista_empresas = lista_projetos = []
    if 'lista_empresas' not in request.session:
        pmo = Pmo()
        user = User()
        user.autentica_usuario(request)
        pmo.obter_projetos(request)
        lista_empresas = request.session['lista_empresas'] = pmo.lista_empresas
        lista_projetos = request.session['lista_projetos'] = pmo.lista_projetos
    lista_empresas = request.session['lista_empresas']
    lista_projetos = request.session['lista_projetos']
    ctx = {'empresas' : lista_empresas, 'projetos' : lista_projetos}
    return render_to_response('projetos.html', ctx, context_instance=RequestContext(request))

def error(request):
    """Error view"""
    messages = get_messages(request)
    return render_to_response('error.html', {'version': version, 'messages': messages}, RequestContext(request))

def login_error(request):
    error_message = 'Tudo bem se voce nÃ£o quer autorizar o acesso Ã s suas planilhas. Se mudar de idÃ©ia estou te esperando.'
    return custom_error(request, error_message)

def complete(request, backend):
    return social_complete(request, backend)

def custom_error(request, error_message):
    return render_to_response('error/custom.html', {'error_message': error_message}, context_instance=RequestContext(request))

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')