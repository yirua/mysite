from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run_flow
#import oauth2client.tools
from oauth2client.file import Storage

CLIENT_ID = '636360490404-b11gcs1ed7jgpand59dfk1tpspb56oih.apps.googleusercontent.com'
CLIENT_SECRET = 'GoogleSheetTest-64c073e738fb.json'

flow = OAuth2WebServerFlow(
          client_id = CLIENT_ID,
          client_secret = CLIENT_SECRET,
          scope = 'https://spreadsheets.google.com/feeds https://docs.google.com/feeds',
          redirect_uri = 'http://example.com/auth_return'
       )

storage = Storage('creds.data')
credentials = run_flow(flow, storage)
print "access_token: %s" % credentials.access_token