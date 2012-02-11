import gdata.spreadsheet.service
from horasdsconapp.pmo.pmo import Pmo
import settings, re, sys, urllib
from unicodedata import normalize
from settings import util
import gdata.service
import gdata.spreadsheet
from social_auth.models import UserSocialAuth
import gdata.spreadsheets.client
import gdata.gauth
import gdata.docs.data
import gdata.docs.client
from gdata.spreadsheet.text_db import DatabaseClient

class GoogleSpreadsheet:

    def __init__(self, request):
        socialuser = UserSocialAuth.objects.get(user=request.user)
        access_token=socialuser.extra_data['access_token']
        self.token = self.GetOAuthToken(access_token)
        self.clientSpr = gdata.spreadsheet.service.SpreadsheetsService()
        self.clientDB = DatabaseClient()
        self.clientDocs = gdata.docs.client.DocsClient(source='horasdscon_app')
        self.clientDocs.http_client.debug = False
        self.clientSpr.auth_token = self.token
        self.clientDocs.auth_token = self.token
        SCOPES = ['https://spreadsheets.google.com/feeds/', 'https://docs.google.com/feeds/', 'https://www.googleapis.com/auth/userinfo#email']
        oauth_input_params = gdata.auth.OAuthInputParams(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, settings.util.getEntry('google_oauth', 'CONSUMER_KEY'), consumer_secret=settings.util.getEntry('google_oauth', 'CONSUMER_SECRET'))
        oauth_token = gdata.auth.OAuthToken(key=self.token.token, secret=self.token.token_secret, scopes=SCOPES, oauth_input_params=oauth_input_params)
        self.clientDB._GetSpreadsheetsClient().SetOAuthInputParameters(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, settings.util.getEntry('google_oauth', 'CONSUMER_KEY'), consumer_secret=settings.util.getEntry('google_oauth', 'CONSUMER_SECRET'))
        self.clientDB._GetDocsClient().SetOAuthInputParameters(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, settings.util.getEntry('google_oauth', 'CONSUMER_KEY'), consumer_secret=settings.util.getEntry('google_oauth', 'CONSUMER_SECRET'))
        self.clientDB._GetDocsClient().SetOAuthToken(oauth_token)

    def GetOAuthToken(self, access_token):
        oauth_token = '1/DRcGn0-Myv8DXw3tYTINobpwUMfwcRezINeOa6vW-qE'
        oauth_token_secret = 'aSlyuQYUjVhUFu-DhrF3hmUp'
        #oauth_token_secret = re.search(r'oauth_token_secret=(.*)&oauth_token=(.*)', access_token).group(1)
        #oauth_token = re.search(r'oauth_token_secret=(.*)&oauth_token=(.*)', access_token).group(2)
        #oauth_token_secret = urllib.unquote(oauth_token_secret)
        #oauth_token = urllib.unquote(oauth_token)
        return gdata.gauth.OAuthHmacToken(
            settings.util.getEntry('google_oauth', 'CONSUMER_KEY'),
            settings.util.getEntry('google_oauth', 'CONSUMER_SECRET'),
            oauth_token,
            oauth_token_secret,
            gdata.gauth.ACCESS_TOKEN,
            next=None,
            verifier=None)

    def ExtractKey(self, entry):
        return entry.id.text.split('/')[-1]

    def FindKeyOfEntryNamed(self, feed, name, kind='spreadsheet'):
        entry = [e for e in feed.entry if e.title.text == name]
        if not entry:
            raise gdata.Error('Can\'t find %s named %s', kind, name)
        if len(entry) > 1:
            raise gdata.Error('More than one %s named %s', kind, name)
        return self.ExtractKey(entry[0])

    def FindKeyOfSpreadsheet(self, name):
        spreadsheets = self.clientSpr.GetSpreadsheets()
        return self.FindKeyOfEntryNamed(spreadsheets, name)

    def FindKeyOfWorksheet(self, key, name):
        worksheets = self.clientSpr.GetWorksheets(key)
        return self.FindKeyOfEntryNamed(worksheets, name, 'worksheet')

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
        db = self.clientDB.CreateDatabase(settings.NOME_PLANILHA_HORAS)
        tabela = db.CreateTable('addresses', ['a','b','c','d'])


        dados = {'usuariopmo':usuario_pmo, 'senhapmo':senha_pmo, 'idcolaborador':colaborador.id, 'nomecolaborador':colaborador.nome}
        row = tabela.AddRecord(dados)
        tabela = db.GetTables(name='Sheet 1')[0]
        tabela.Delete()