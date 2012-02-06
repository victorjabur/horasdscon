#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
from django.core.context_processors import csrf
from django.forms.fields import Field
from django.views.decorators.csrf import csrf_protect

from social_auth.views import complete as social_complete

from django.contrib.auth import logout as auth_logout
from django.contrib.messages.api import get_messages

from social_auth import __version__ as version

from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from forms import CriarPlanilha
from horasdsconapp.google.spreadsheet import GoogleSpreadsheet
import settings

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
    googleSpr = GoogleSpreadsheet(request)
    if googleSpr.planilha_existe():
        ctx = {'version': version,
               'last_login': request.session.get('social_auth_last_login_backend')}
        return render_to_response('done.html', ctx, RequestContext(request))
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
            pass
        else:
            ctx = {'form': form,}
            return render_to_response('criarplanilha.html', ctx, context_instance=RequestContext(request))

def error(request):
    """Error view"""
    messages = get_messages(request)
    return render_to_response('error.html', {'version': version, 'messages': messages}, RequestContext(request))

def complete(request, backend):
    error = request.GET.get('error')
    if error != None and len(error) > 0:
        if error == 'access_denied':
            error_message = 'Tudo bem se voce n�o quer autorizar o acesso �s suas planilhas. Se mudar de id�ia estou te esperando.'
        else:
            error_message = 'Um erro de autentica��o ocorreu com o Google Docs: ' + error
        return custom_error(request, error_message)
    return social_complete(request, backend)

def custom_error(request, error_message):
    return render_to_response('error/custom.html', {'error_message': error_message}, context_instance=RequestContext(request))

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')