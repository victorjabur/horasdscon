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
from gdata.spreadsheet.text_db import DatabaseClient

class GoogleSpreadsheet:

    def __init__(self, request):
        socialuser = UserSocialAuth.objects.get(user=request.user)
        self.clientSpr = gdata.spreadsheet.service.SpreadsheetsService()
        self.clientDB = DatabaseClient()
        self.clientDocs = gdata.docs.client.DocsClient(source='horasdscon_app')
        self.clientDocs.http_client.debug = False
        self.token = gdata.gauth.OAuthHmacToken(
            settings.util.getEntry('google_oauth', 'CONSUMER_KEY'),
            settings.util.getEntry('google_oauth', 'CONSUMER_SECRET'),
            settings.util.getEntry('google_oauth', 'TOKEN_KEY'),
            settings.util.getEntry('google_oauth', 'TOKEN_SECRET'),
            gdata.gauth.ACCESS_TOKEN,
            next=None,
            verifier=None)
        self.clientSpr.auth_token = self.token
        self.clientDocs.auth_token = self.token
        oauth_input_params = gdata.auth.OAuthInputParams(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, settings.util.getEntry('google_oauth', 'CONSUMER_KEY'), consumer_secret=settings.util.getEntry('google_oauth', 'CONSUMER_SECRET'))
        oauth_token = gdata.auth.OAuthToken(key=settings.util.getEntry('google_oauth', 'TOKEN_KEY'), secret=settings.util.getEntry('google_oauth', 'TOKEN_SECRET'), scopes=settings.GOOGLE_OAUTH_EXTRA_SCOPE, oauth_input_params=oauth_input_params)
        self.clientDB._GetSpreadsheetsClient().SetOAuthInputParameters(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, settings.util.getEntry('google_oauth', 'CONSUMER_KEY'), consumer_secret=settings.util.getEntry('google_oauth', 'CONSUMER_SECRET'))
        self.clientDB._GetDocsClient().SetOAuthInputParameters(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, settings.util.getEntry('google_oauth', 'CONSUMER_KEY'), consumer_secret=settings.util.getEntry('google_oauth', 'CONSUMER_SECRET'))
        self.clientDB._GetSpreadsheetsClient().SetOAuthToken(oauth_token)
        self.clientDB._GetDocsClient().SetOAuthToken(oauth_token)
        self.keyPlanilha = ''
        self.keyWorksheet = ''

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

    def FindKeyOfWorksheet(self, name):
        worksheets = self.clientSpr.GetWorksheets(self.keyPlanilha)
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
        tabela = db.CreateTable('config', ['usuariopmo','senhapmo','idcolaborador','nomecolaborador'])
        dados = {'usuariopmo':usuario_pmo, 'senhapmo':senha_pmo, 'idcolaborador':colaborador.id, 'nomecolaborador':colaborador.nome}
        row = tabela.AddRecord(dados)
        db.GetTables(   )

        #        resource = gdata.docs.data.Resource('spreadsheet', settings.NOME_PLANILHA_HORAS)
        #        media = gdata.data.MediaSource()
        #        media.SetFileHandle(settings.PATH_PLANILHA_HORAS_TEMPLATE, 'application/vnd.ms-excel')
        #        planilha = self.clientDocs.CreateResource(resource, media=media)
        #        self.keyPlanilha = self.FindKeyOfSpreadsheet('horas_victor')
        #        self.keyWorksheet = self.FindKeyOfWorksheet('Janeiro12')
        #        headers = {'A':'usuario_pmo', 'B':'senha_pmo', 'C':'id_colaborador', 'D':'nome_colaborador'}
        #        self.clientSpr.add_table(self.keyPlanilha, 'configuracoes', 'config', 'config', 1, 0, 2, 'overwrite', headers)
        #        dados = {'usuario_pmo':usuario_pmo, 'senha_pmo':senha_pmo, 'id_colaborador':colaborador.id, 'nome_colaborador':colaborador.nome}
        #        self.clientSpr.add_record(self.keyPlanilha, '0', dados)
        #        self.clientSpr.add_record(self.keyPlanilha, '0', dados)
        #        records = self.clientSpr.get_records(self.keyPlanilha, '0')
        #        cells = self.clientSpr.get_cells(self.keyPlanilha, self.keyWorksheet)

        print usuario_pmo
        #print senha_pmo
        #print colaborador.id
        #print colaborador.nome
