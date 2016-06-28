# http://tutorial.djangogirls.org/en/installation/   # reference
# install python2.7
## virtualenv -p /usr/bin/python2.7 ./virtual_env/venv
# pip install django
# pip install gspread
# pip install gdata   or download the package into the path Downloads/gdata/gdata-python-client-master/  sudo ./setup.py install
# https://pythonhosted.org/gdata/installation.html
# pip install psycopg2
# pip install --upgrade oauth2client

################### django-sheets get the google sheet contents to show up like a table
#### https://django-sheets.readthedocs.org/en/latest/usage.html 
# pip install django-sheets
# Add sheets to INSTALLED_APPS in settings.py:
''' 
INSTALLED_APPS = (
    ...
    'sheets',
    ...
)
'''
#!/usr/bin/python

import gdata.docs.service
from gdata.spreadsheets.client import SpreadsheetsClient
import gdata.gauth


# Create a client class which will make HTTP requests with Google Docs server.
client = gdata.docs.service.DocsService()
# Authenticate using your Google Docs email address and password.

client.Download('https://docs.google.com/spreadsheets/d/1mu9CVYUIi81Ntag5eIEzJEUV8RmWT_V0DCzmh9lqwAs/edit#gid=1489986476','/Users/yiweisun/Downloads/gdata/iah1_metadata_2016')
documents_feed = client.GetDocumentListFeed()


################################################################################ from https://gist.github.com/egor83/4634422#file-google_spreadsheets-py
'''
client = gdata.spreadsheets.client.SpreadsheetsClient()

token = GetAuthSubUrl()
token.authorize(client)

sps = client.GetSpreadsheets()
print len(sps.entry) # shows how many spreadsheets you have

sprd_key = '1ZPIYJtaPNIEpT_rvvR3WfKvXYx1_p2vZtHycCPUUaJg' # a certain key
wss = client.GetWorksheets(sprd_key) # get a list of all worksheets in this spreadsheet, to look around for info in a debugger
ws = client.GetWorksheet(sprd_key, 'od6') # get the first worksheet in a spreadsheet; seems 'od6' is always used as a WS ID of the first worksheet
def GetAuthSubUrl():
  next = 'http://www.example.com/myapp.py'
  scopes = ['http://docs.google.com/feeds/', 'https://docs.google.com/feeds/']
  secure = False  # set secure=True to request a secure AuthSub token
  session = True
  return gdata.gauth.generate_auth_sub_url(next, scopes, secure=secure, session=session)

print '<a href="%s">Login to your Google account</a>' % GetAuthSubUrl()
'''
######################################### to get the googlesheet contents method succeed...

import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://spreadsheets.google.com/feeds']
path_to_json = '/Users/yiweisun/Downloads/GoogleSheetTest-d112a30fe1a8.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(path_to_json, scope)
gc = gspread.authorize(credentials)

#wks = gc.open("iah1_metadata_2016").sheet1  #gspread.exceptions.SpreadsheetNotFound
#wks = gc.open("iah1_metadata_2016") #gspread.exceptions.SpreadsheetNotFound
#inDjango, method
##### gspread    http://www.indjango.com/access-google-sheets-in-python-using-gspread/


sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1mu9CVYUIi81Ntag5eIEzJEUV8RmWT_V0DCzmh9lqwAs/edit#gid=1489986476')

sh1 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1ZPIYJtaPNIEpT_rvvR3WfKvXYx1_p2vZtHycCPUUaJg/edit#gid=2130071960')
sh1 = gc.open_by_key('1ZPIYJtaPNIEpT_rvvR3WfKvXYx1_p2vZtHycCPUUaJg')
##### gspread    http://www.indjango.com/access-google-sheets-in-python-using-gspread/
#worksheet = sh.get_worksheet(4)
worksheet=sh1.worksheet('data_collector')
worksheet_list = sh.worksheets()
# worksheet_list
values_list = worksheet.row_values(1)
values_list_2 = worksheet.row_values(2)
values_list_3 = worksheet.row_values(3)

worksheet_1 = sh1.get_worksheet(4)
worksheet_list_1 = sh.worksheets()
worksheet_list_1
# before to do the openall(), you have to share the documents with the client email that in the downloaded json file. for example, scenic-setup-128014@appspot.gserviceaccount.com, which 
# is NOT the gmail email account. 
sh_all = gc.openall()
#######################################step 1 from http://heinrichhartmann.com/2015/05/17/Using-the-Google-Drive-Spreadsheet-API.html
