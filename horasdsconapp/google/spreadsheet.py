import gdata.spreadsheet.service
from horasdsconapp.pmo.pmo import Pmo
import settings
from settings import util
import gdata.service
import gdata.spreadsheet
from social_auth.models import UserSocialAuth
import gdata.spreadsheets.client
import gdata.gauth
import gdata.docs.data
import gdata.docs.client
import gdata.client as gclient
from gdata.spreadsheet.text_db import DatabaseClient


class GoogleSpreadsheet:

    def __init__(self, request):
        socialuser = UserSocialAuth.objects.get(user=request.user)
        self.token = gdata.gauth.OAuth2Token(client_id=util.getEntry('google_oauth2','CLIENT_ID'),
            client_secret=util.getEntry('google_oauth2','CLIENT_SECRET'),
            scope=settings.GOOGLE_OAUTH_EXTRA_SCOPE,
            user_agent='horasdscon',
            access_token=socialuser.extra_data['access_token'],
            refresh_token=socialuser.extra_data['refresh_token'])
        self.clientSpr = gdata.spreadsheets.client.SpreadsheetsClient()
        self.token.authorize(self.clientSpr)
        self.clientDocs = gdata.docs.client.DocsClient(source='horasdscon_app')
        self.clientDocs.http_client.debug = False
        self.token.authorize(self.clientDocs)

    def ExtractKey(self, entry):
        return entry.id.text.split('/')[-1]

    def FindKeyOfEntryNamed(self, feed, name, kind='spreadsheet'):
        entry = [e for e in feed.entry if e.title.text == name]
        if not entry:
            raise Error('Can\'t find %s named %s', kind, name)
        if len(entry) > 1:
            raise Error('More than one %s named %s', kind, name)
        return self.ExtractKey(entry[0])

    def FindKeyOfSpreadsheet(self, name):
        spreadsheets = self.clientSpr.GetSpreadsheets()
        return self.FindKeyOfEntryNamed(spreadsheets, name)

    def planilha_existe(self):
        try:
            self.FindKeyOfSpreadsheet(settings.NOME_PLANILHA_HORAS)
            return True
        except:
            return False

    def criar_planilha(self, usuario_pmo, senha_pmo):
        pmo = Pmo()
        loginInfo = pmo.login(usuario_pmo, senha_pmo)
        colaborador = pmo.extrairColaboradorFromPagina(loginInfo.pagina)
        resource = gdata.docs.data.Resource('spreadsheet', settings.NOME_PLANILHA_HORAS)
        planilha = self.clientDocs.CreateResource(resource)
        print usuario_pmo
        print senha_pmo
        print colaborador.id
        print colaborador.nome
