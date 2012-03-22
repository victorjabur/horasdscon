from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

@dajaxice_register
def updatecomboprojetos(request, option):
    projetos = []
    option = str(option.encode('utf-8'))
    lista_projetos = request.session['lista_projetos']
    for projeto in lista_projetos:
        if projeto.company == option:
            projetos.append(Combo(projeto.projectid, projeto.projectname))
    #return simplejson.dumps(projetos)
    return '[{ text: "Item14566", value: "1" },{ text: "Item234355",value: "2" }]'

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


class Combo:
    def __init__(self, text='', value=''):
        self.text = text
        self.value = value