from dajax.core import Dajax
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

@dajaxice_register
def updatecomboprojetos(request, option):
    dajax = Dajax()
    options = [ ['Madrid','Barcelona','Vitoria','Burgos'],
        ['Paris','Evreux','Le Havre','Reims'],
        ['London','Birmingham','Bristol','Cardiff'],]
    out = ''
    for o in options[int(option)]:
        out += "<option value='#'>%s" % (o)

    #dajax.assign('#combo2','innerHTML',out)
    #return dajax.json()
    return simplejson.dumps({'message':'Hello World'})