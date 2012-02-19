from horasdsconapp.google.spreadsheet import GoogleSpreadsheet
from horasdsconapp.pmo.pmo import Pmo
import settings

class User:
    def autentica_usuario(self, request):
        if not request.session.get('cookie_pmo', False):
            googlespr = GoogleSpreadsheet(request)
            pmo = Pmo()
            db = googlespr.clientDB.GetDatabases(name=settings.NOME_PLANILHA_HORAS)[0]
            tabela = db.GetTables(name='config')[0]
            row = tabela.GetRecord(row_number=1)
            usuario_pmo = row.content['usuariopmo']
            senha_pmo = row.content['senhapmo']
            request.session['cookie_pmo'] = pmo.login(usuario_pmo, senha_pmo).cookies
            request.session['usuario_pmo'] = usuario_pmo
            request.session['senha_pmo'] = senha_pmo
