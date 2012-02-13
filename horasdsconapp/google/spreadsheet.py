import gdata.spreadsheet.service
from horasdsconapp.pmo.pmo import Pmo
import settings, urllib, re, locale, datetime, calendar
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
        pass
        socialuser = UserSocialAuth.objects.get(user=request.user)
        access_token=socialuser.extra_data['access_token']
        self.consumer_key = util.getEntry('google_oauth', 'CONSUMER_KEY')
        self.consumer_secret = util.getEntry('google_oauth', 'CONSUMER_SECRET')
        self.signature_method = gdata.auth.OAuthSignatureMethod.HMAC_SHA1
        self.token = self.GetOAuthToken(access_token)
        self.clientDB = DatabaseClient()
        self.autenticaClientService(self.clientDB._GetSpreadsheetsClient())
        self.autenticaClientService(self.clientDB._GetDocsClient())

    def autenticaClientService(self, client):
        oauth_input_params = gdata.auth.OAuthInputParams(self.signature_method, self.consumer_key, consumer_secret=self.consumer_secret)
        oauth_token = gdata.auth.OAuthToken(key=self.token.token, secret=self.token.token_secret, scopes=settings.GOOGLE_OAUTH_EXTRA_SCOPE, oauth_input_params=oauth_input_params)
        client.SetOAuthInputParameters(self.signature_method, self.consumer_key, consumer_secret=self.consumer_secret)
        client.SetOAuthToken(oauth_token)

    def GetOAuthToken(self, access_token):
        pattern = 'oauth_token_secret=(.*)&oauth_token=(.*)'
        oauth_token_secret = urllib.unquote(re.search(pattern, access_token).group(1))
        oauth_token = urllib.unquote(re.search(pattern, access_token).group(2))
        return gdata.gauth.OAuthHmacToken(
            self.consumer_key,
            self.consumer_secret,
            oauth_token,
            oauth_token_secret,
            gdata.gauth.ACCESS_TOKEN,
            next=None,
            verifier=None)

    def planilha_existe(self):
        return len(self.clientDB.GetDatabases(name=settings.NOME_PLANILHA_HORAS)) > 0

    def criar_planilha(self, usuario_pmo, senha_pmo):
        pmo = Pmo()
        loginInfo = pmo.login(usuario_pmo, senha_pmo)
        colaborador = pmo.extrairColaboradorFromPagina(loginInfo.pagina)
        db = self.clientDB.CreateDatabase(settings.NOME_PLANILHA_HORAS)
        colunas = ['usuariopmo','senhapmo','idcolaborador','nomecolaborador']
        tabela = db.CreateTable('config', colunas)
        dados = {colunas[0]:usuario_pmo, colunas[1]:senha_pmo, colunas[2]:colaborador.id, colunas[3]:colaborador.nome}
        row = tabela.AddRecord(dados)
        self.criarWorksheetMesCorrente()
        tabela = db.GetTables(name='Sheet 1')[0]
        tabela.Delete()

    def criarWorksheetMesCorrente(self):
        now = datetime.datetime.now()
        mes_corrente = self.GetMesCorrente()
        nome_mes_corrente =  now.strftime('%B').capitalize()
        ano_corrente = str(now.year)
        colunas = ['data', 'diasemana', 'horaentrada', 'horasaida', 'taskid', 'descricaotask', 'idregistropmo']
        db = self.clientDB.GetDatabases(name=settings.NOME_PLANILHA_HORAS)[0]
        tabela = db.CreateTable(nome_mes_corrente + ano_corrente, colunas)
        for data in mes_corrente:
            datastr = data.strftime('%Y-%m-%d')
            diasemanastr = unicode(data.strftime("%A").capitalize(), 'iso-8859-1')
            dados = {colunas[0]:datastr, colunas[1]:diasemanastr, colunas[2]:'00:00', colunas[3]:'00:00',
                     colunas[4]:'', colunas[5]:'', colunas[6]:''}
            row = tabela.AddRecord(dados)
            row = tabela.AddRecord(dados)

    def GetMesCorrente(self):
        now = datetime.datetime.now()
        lista_datas = []
        calendar.setfirstweekday(calendar.SUNDAY)
        mes_atual = calendar.monthcalendar(now.year, now.month)
        for semana in mes_atual:
            for dia in semana:
                if dia > 0:
                    data = datetime.date(now.year, now.month, dia)
                    lista_datas.append(data)
        return lista_datas