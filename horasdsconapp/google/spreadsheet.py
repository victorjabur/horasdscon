import gdata.spreadsheet.service
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
        self.gd_client = gdata.spreadsheets.client.SpreadsheetsClient()
        self.token.authorize(self.gd_client)

    def ExtractKey(self, entry):
        return entry.id.text.split('/')[-1]

    def FindKeyOfEntryNamed(self, feed, name, kind='spreadsheet'):
        entry = [e for e in feed.entry if e.title.text == name]
        if not entry:
            raise Error('Can\'t find %s named %s', kind, name)
        if len(entry) > 1:
            raise Error('More than one %s named %s', kind, name)
        return self.ExtractKey(entry[0])

    def planilha_existe(self):
        feed = self.gd_client.GetSpreadsheets()
        try:
            self.FindKeyOfEntryNamed(feed, settings.NOME_PLANILHA_HORAS)
            return True
        except:
            return False

    def criar_planilha(self):
        client = gdata.docs.client.DocsClient(source='horasdscon_app')
        client.http_client.debug = True
        self.token.authorize(client)
        resource = gdata.docs.data.Resource('spreadsheet', settings.NOME_PLANILHA_HORAS)
        planilha = client.CreateResource(resource)