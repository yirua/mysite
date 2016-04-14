# refresh_token? 4/LBAW3b-ErbZMou5HjUPVTDeCghlKaZUw52G-VnNfdN0#

import requests, gspread
#from oauth2client.appengine import AppAssertionCredentials
import oauth2client.SignedJwtAssertionCredentials


def authenticate_google_docs():
    f = file(os.path.join('/Users/yiweisun/Downloads/gdata/GoogleSheetTest-64c073e738fb.json'), 'rb')
    SIGNED_KEY = f.read()
    f.close()
    scope = ['https://spreadsheets.google.com/feeds', 'https://docs.google.com/feeds']
    credentials = SignedJwtAssertionCredentials('yiweis@gmail.com', SIGNED_KEY, scope)

    data = {
        'refresh_token' : '<refresh-token-copied>',
        'client_id' : '<client-id-copied>',
        'client_secret' : '<client-secret-copied>',
        'grant_type' : 'refresh_token',
    }

    r = requests.post('https://accounts.google.com/o/oauth2/token', data = data)
    credentials.access_token = ast.literal_eval(r.text)['4/LBAW3b-ErbZMou5HjUPVTDeCghlKaZUw52G-VnNfdN0#']

    gc = gspread.authorize(credentials)
    return gc