#! /usr/bin/python
# coding: utf-8

from django.http import HttpResponse
from django.utils import simplejson
from horasdsconapp.Util import Util
import re

class Kendo:

    def __init__(self):
        self.util = Util()

    def get_combobox_from_listaempresa(self, lista_empresa):
        lista_items = []
        for empresa in lista_empresa:
            lista_items.append(ItemCombo('IdEmpresa', empresa.company_id, 'NomeEmpresa', empresa.company_name))
        return Combo(lista_items)

    def get_combobox_from_listaprojetos(self, lista_projetos):
        lista_items = []
        for projeto in lista_projetos:
            lista_items.append(ItemCombo('IdProjeto', projeto.projectid, 'NomeProjeto', projeto.projectid + " - " + projeto.projectname))
        return Combo(lista_items)

    def get_combobox_from_listatarefas(self, lista_tarefas):
        lista_items = []
        for tarefa in lista_tarefas:
            lista_items.append(ItemCombo('IdTarefa', tarefa.id_tarefa, 'NomeTarefa', tarefa.id_tarefa + " - " + tarefa.nome_tarefa))
        return Combo(lista_items)

    def get_json_kendoui(self, request, combobox):
        if combobox != None and len(combobox.list_items) > 0:
            list_items = []
            if '$filter' in request.GET:
                filter = request.GET['$filter']
                filterfunction = re.search(r"(\w*)", filter).group(1).encode("utf-8")
                stringfilter = re.search(r"'(.*)'", filter).group(1).encode("utf-8")
                combobox_filtrado = self.filtra_combo(request, filterfunction, combobox, stringfilter)
                if combobox_filtrado != None:
                    combobox = combobox_filtrado
            for item in combobox.list_items:
                dict = {}
                dict[item.label_value] = item.value
                dict[item.label_text] = item.text
                list_items.append(dict)
            data = simplejson.dumps({'d':{'results':list_items, '__count' : str(len(list_items))}})
        else:
            data = simplejson.dumps({'d':{'results':[], '__count' : '0'}})
        return HttpResponse(request.GET['$callback'] + '(' + data + ')',mimetype='text/javascript;charset=utf-8')

    def filtra_combo(self, request, funcao, combobox, stringfiltro):
        if funcao == 'substringof':
            lista_filtrada = []
            for item in combobox.list_items:
                if self.util.is_string_equals_ignorecase(item.text, stringfiltro):
                    lista_filtrada.append(item)
            return Combo(lista_filtrada)

class ItemCombo:
    def __init__(self, label_value='', value='', label_text='', text=''):
        self.label_value = label_value
        self.value = value
        self.label_text = label_text
        self.text = text

class Combo:
    def __init__(self, list_items=[]):
        self.list_items = list_items