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
from horasdsconapp.json import kendo
from horasdsconapp.json.kendo import Kendo
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
    kendo = Kendo()
    combo_empresas = None
    if 'lista_empresas' in request.session:
        if 'combo_empresas' not in request.session:
            combo_empresas = kendo.get_combobox_from_listaempresa(request.session['lista_empresas'])
            request.session['combo_empresas'] = combo_empresas
        else:
            combo_empresas = request.session['combo_empresas']
    return kendo.get_json_kendoui(request, combo_empresas)

@login_required
def ajax_projetos(request):
    kendo = Kendo()
    if 'lista_projetos' in request.session:
        filter = str(request.GET['$filter'].encode('utf-8'))
        if filter.find('(') == -1:
            lista_projetos = request.session['lista_projetos']
            option = int(re.search(r"IdEmpresa eq '(.*)'", filter).group(1))
            lista_projetos_selecao = []
            for projeto in lista_projetos:
                if projeto.company_id == option or option == 0:
                    lista_projetos_selecao.append(projeto)
            request.session['lista_projetos_selecao'] = lista_projetos_selecao
            combo_projetos = kendo.get_combobox_from_listaprojetos(lista_projetos_selecao)
        else:
            combo_projetos = kendo.get_combobox_from_listaprojetos(request.session['lista_projetos_selecao'])
    return kendo.get_json_kendoui(request, combo_projetos)

@login_required
def ajax_tarefas(request):
    kendo = Kendo()
    filter = str(request.GET['$filter'].encode('utf-8'))
    if filter.find('(') == -1:
        option = int(re.search(r"IdProjeto eq '(.*)'", filter).group(1))
        pmo = Pmo()
        lista_tarefas = pmo.extrairTarefasFromIdProjeto(request, option)
        request.session['lista_tarefas'] = lista_tarefas
        combo_tarefas = kendo.get_combobox_from_listatarefas(lista_tarefas)
    else:
        combo_tarefas = kendo.get_combobox_from_listatarefas(request.session['lista_tarefas'])
    return kendo.get_json_kendoui(request, combo_tarefas)

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