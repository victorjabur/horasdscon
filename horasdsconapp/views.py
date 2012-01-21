import logging
import httplib2

from django.contrib.auth import logout as auth_logout
from django.contrib.messages.api import get_messages

from social_auth import __version__ as version

import settings
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from oauth2client.django_orm import Storage
from oauth2client.client import OAuth2WebServerFlow
from apiclient.discovery import build

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

def handle_error500(request, template_name='error/500.html'):
    return render_to_response(template_name, context_instance = RequestContext(request))

def handle_error404(request, template_name='error/404.html'):
    return render_to_response(template_name, context_instance = RequestContext(request))

def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return HttpResponseRedirect('done')
    else:
        return render_to_response('home.html', {'version': version},
            RequestContext(request))

@login_required
def done(request):
    """Login complete view, displays user data"""
    ctx = {'version': version,
           'last_login': request.session.get('social_auth_last_login_backend')}
    return render_to_response('done.html', ctx, RequestContext(request))


def error(request):
    """Error view"""
    messages = get_messages(request)
    return render_to_response('error.html', {'version': version,
                                             'messages': messages},
        RequestContext(request))

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')

@login_required
def index(request):
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        flow = OAuth2WebServerFlow(
            client_id = settings.util.getEntry('google_oauth', 'CLIENT_ID', settings.PYTHON_CONF),
            client_secret = settings.util.getEntry('google_oauth', 'CLIENT_SECRET', settings.PYTHON_CONF),
            scope='https://spreadsheets.google.com/feeds/',
            user_agent='lancamento_horas_dscon/1.0',
        )
        authorize_url = flow.step1_get_authorize_url(STEP2_URI)
        f = FlowModel(id=request.user, flow=flow)
        f.save()
        return render_to_response('index.html', {'authorize_url': authorize_url}, context_instance = RequestContext(request))
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build("feeds", "v1", http=http)
        gd_client = service.SpreadsheetsService()
        feed = gd_client.GetSpreadsheetsFeed()
        logging.info(feed)
        return render_to_response('welcome.html', {'feed': feed,})

@login_required
def auth_return(request):
    error = request.GET.get('error')
    if error != None and len(error) > 0:
        if error == 'access_denied':
            error_message = 'Tudo bem se voce nao quer autorizar o acesso as suas planilhas. Se mudar de ideia estou te esperando.'
        else:
            error_message = 'Um erro de autenticacao ocorreu com o Google Docs: ' + error
        return render_to_response('error/custom.html', {'error_message': error_message}, context_instance = RequestContext(request))
    try:
        f = FlowModel.objects.get(id=request.user)
        credential = f.flow.step2_exchange(request.REQUEST)
        storage = Storage(CredentialsModel, 'id', request.user, 'credential')
        storage.put(credential)
        f.delete()
        return HttpResponseRedirect("/")
    except FlowModel.DoesNotExist:
        pass
