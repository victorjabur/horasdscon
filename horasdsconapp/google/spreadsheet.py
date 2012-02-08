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
#        pmo = Pmo()
#        loginInfo = pmo.login(usuario_pmo, senha_pmo)
#        colaborador = pmo.extrairColaboradorFromPagina(loginInfo.pagina)
#        resource = gdata.docs.data.Resource('spreadsheet', settings.NOME_PLANILHA_HORAS)
#        media = gdata.data.MediaSource()
#        media.SetFileHandle(settings.PATH_PLANILHA_HORAS_TEMPLATE, 'application/vnd.ms-excel')
#        planilha = self.clientDocs.CreateResource(resource, media=media)
        self.keyPlanilha = self.FindKeyOfSpreadsheet(settings.NOME_PLANILHA_HORAS)
        self.keyWorksheet = self.FindKeyOfWorksheet('config')
#        headers = {'A':'usuario_pmo', 'B':'senha_pmo', 'C':'id_colaborador', 'D':'nome_colaborador'}
#        self.clientSpr.add_table(self.keyPlanilha, 'configuracoes', 'config', 'config', 1, 0, 2, 'overwrite', headers)
#        dados = {'usuario_pmo':usuario_pmo, 'senha_pmo':senha_pmo, 'id_colaborador':colaborador.id, 'nome_colaborador':colaborador.nome}
#        self.clientSpr.add_record(self.keyPlanilha, '0', dados)
#        self.clientSpr.add_record(self.keyPlanilha, '0', dados)
#        records = self.clientSpr.get_records(self.keyPlanilha, '0')
        cells = self.clientSpr.get_cells(self.keyPlanilha, self.keyWorksheet)
        self.clientSpr


        print usuario_pmo
        #print senha_pmo
        #print colaborador.id
        #print colaborador.nome
