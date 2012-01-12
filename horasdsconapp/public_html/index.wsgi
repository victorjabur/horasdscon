import os, sys, site
from ConfigParser import RawConfigParser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_CONF = os.path.abspath(os.path.join(BASE_DIR, '../../python_conf/horasdscon/settings.ini'))
config = RawConfigParser()
config.read(PYTHON_CONF)

RAIZ_LOCAL = config.get('geral', 'RAIZ_LOCAL')
RAIZ_REMOTA = config.get('geral', 'RAIZ_REMOTA')
VIRTUALENV_LOCAWEB = config.get('geral', 'VIRTUALENV_LOCAWEB')
NOME_PROJETO = config.get('geral', 'NOME_PROJETO')

site.addsitedir(RAIZ_REMOTA + '/.python/lib')
site.addsitedir(VIRTUALENV_LOCAWEB)
import django.core.handlers.wsgi
sys.path.append(RAIZ_REMOTA + '/wsgi_apps/' + NOME_PROJETO)
sys.path.append(RAIZ_LOCAL + '/' + NOME_PROJETO)
os.environ['DJANGO_SETTINGS_MODULE']='settings'
application = django.core.handlers.wsgi.WSGIHandler()
