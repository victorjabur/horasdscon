from dajax.core import Dajax
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

@dajaxice_register
def updatecomboprojetos(request, option):
    #dajax = Dajax()
    option = str(option.encode('utf-8'))
    lista_projetos = request.session['lista_projetos']
    out = ''
    for projeto in lista_projetos:
        if projeto.company == option:
            out += "<option value='%s'>%s" % (projeto.projectname, projeto.projectname)
    #dajax.assign('#combo2','innerHTML',out)
    #return dajax.json()
    return simplejson.dumps({'result':out})

@dajaxice_register
def dajaxice_example(request):
    return simplejson.dumps({'message':'Hello from Python!'})

@dajaxice_register
def example1(request):
    """ First simple example """
    return simplejson.dumps({'message': 'hello world'})

@dajaxice_register
def example2(request):
    """ Second simple example """
    return simplejson.dumps({'numbers': [1, 2, 3]})

@dajaxice_register
def example3(request, data, name):
    result = sum(map(int, data))
    return simplejson.dumps({'result': result})

@dajaxice_register
def error_example(request):
    raise Exception("Some Exception")
