## virtualenv -p /usr/bin/python2.7 ./virtual_env/venv
# pip install django
# pip install gspread
# pip install gdata   or download the package into the path Downloads/gdata/gdata-python-client-master/  sudo ./setup.py install
# https://pythonhosted.org/gdata/installation.html

#!/usr/bin/python
import gdata.docs.service

# Create a client class which will make HTTP requests with Google Docs server.
client = gdata.docs.service.DocsService()
# Authenticate using your Google Docs email address and password.
client.ClientLogin('yiweis@gmail.com', 'Sunyr1069')

#c = gspread.Client(auth=('yiweis@gmail.com', 'Sunyr1069'))
import gspread
from oauth2client.service_account import ServiceAccountCredentials
c = gspread.Client(auth=('yiweis@gmail.com', 'Sunyr1069'))

scope = ['https://spreadsheets.google.com/feeds']
#in Credentials, choose Compute Engine default service account
#credentials = ServiceAccountCredentials.from_json_keyfile_name('yiweiProject Test Google Cloud-68c7f7c95ba1.json', scope)

credentials = ServiceAccountCredentials.from_json_keyfile_name('/Users/yiweisun/Downloads/gdata/yiweiProject Test Google Cloud-68c7f7c95ba1.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open_by_url('https://docs.google.com/spreadsheets/d/1ZPIYJtaPNIEpT_rvvR3WfKvXYx1_p2vZtHycCPUUaJg/edit#gid=2130071960')

#inDjango, method

# import gspread
# gc = gspread.login('yiweis@gmail.com', 'Sunyr1069') # this one does not work since Dec. 2015, have to use oauth2Client...
# sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1ZPIYJtaPNIEpT_rvvR3WfKvXYx1_p2vZtHycCPUUaJg/edit#gid=1414159729')