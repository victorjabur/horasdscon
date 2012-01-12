from django.template import Context, loader, RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

def handle_error500(request, template_name='error/500.html'):
    return render_to_response(template_name, context_instance = RequestContext(request))

def handle_error404(request, template_name='error/404.html'):
    return render_to_response(template_name, context_instance = RequestContext(request))

def index(request):
    return render_to_response('index.html')
