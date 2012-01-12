import gdata.spreadsheet.service
import gdata.service
import gdata.spreadsheet

def GetAuthSubUrl():
    next = 'http://horasdscon.victorjabur.com'
    scope = 'https://spreadsheets.google.com/feeds/'
    secure = True
    session = True
    gd_client = gdata.spreadsheet.service.SpreadsheetsService()
    return gd_client.GenerateAuthSubURL(next, scope, secure, session);