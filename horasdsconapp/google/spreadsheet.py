from xml.etree import ElementTree
import gdata.spreadsheet.service
import gdata.service
import atom.service
import gdata.spreadsheet
import atom
from social_auth.models import Association


class GoogleSpreadsheet:

    def __init__(self, request, token):
        self.gd_client = gdata.spreadsheet.service.SpreadsheetsService()
        association = Association.objects.get(user=request.user)
        google_session_token=association.handle
        google_secret=association.secret

    def _PromptForSpreadsheet(self):
        feed = self.gd_client.GetSpreadsheetsFeed()
        self._PrintFeed(feed)

    def _PrintFeed(self, feed):
        for i, entry in enumerate(feed.entry):
            if isinstance(feed, gdata.spreadsheet.SpreadsheetsCellsFeed):
                print '%s %s\n' % (entry.title.text, entry.content.text)
            elif isinstance(feed, gdata.spreadsheet.SpreadsheetsListFeed):
                print '%s %s %s' % (i, entry.title.text, entry.content.text)
                # Print this row's value for each column (the custom dictionary is
                # built using the gsx: elements in the entry.)
                print 'Contents:'
                for key in entry.custom:
                    print '  %s: %s' % (key, entry.custom[key].text)
                print '\n',
            else:
                print '%s %s\n' % (i, entry.title.text)