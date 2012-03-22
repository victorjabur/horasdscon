from django.utils import simplejson
lista = []
lista.append({'a':'1', 'b':'2'})
lista.append({'d':'3', 'e':'4'})
print simplejson.dumps(lista)