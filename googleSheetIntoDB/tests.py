from django.test import TestCase
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.http import Http404


from .models import Metadata
from .models import MetadataManager
from .models import Json_path
from .models import Json_path_Manager

# Create your tests here.

class MetadataCreateTests(TestCase):

    def list_to_choose(self):
        googleSheet_listing = []

        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            '/Users/yiweisun/Downloads/GoogleSheetTest-d112a30fe1a8.json', scope)
        gc = gspread.authorize(credentials)

        sh = gc.open_by_url(
            'https://docs.google.com/spreadsheets/d/1mu9CVYUIi81Ntag5eIEzJEUV8RmWT_V0DCzmh9lqwAs/edit#gid=1489986476')

        sh1 = gc.open_by_url(
            'https://docs.google.com/spreadsheets/d/1ZPIYJtaPNIEpT_rvvR3WfKvXYx1_p2vZtHycCPUUaJg/edit#gid=2130071960')

        worksheet = sh.get_worksheet(4)
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

        # why this one only has one object?
        '''for todo_list in sh_all:
            todo_dict = {}

            todo_dict['list_object'] = todo_list

            # todo_dict['item_count'] = todo_list.item_set.count()

            googleSheet_listing.append(todo_dict)

            # return render_to_response('list_to_choose.html', { 'googleSheet_listing': googleSheet_listing })
        '''
        return values_list_3  # googleSheet_listing

    def get_titles_in_db(self):
        return Metadata.objects.all()

    def google_list_to_choose(self):
        try:
            scope = ['https://spreadsheets.google.com/feeds']
            # credentials = ServiceAccountCredentials.from_json_keyfile_name('/Users/yiweisun/Downloads/GoogleSheetTest-d112a30fe1a8.json', scope)
            json_path = '/Users/yiweisun/Downloads/GoogleSheetTest-d112a30fe1a8.json'
            credentials = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
            gc = gspread.authorize(credentials)
            sh_all = gc.openall()

        except gspread.exceptions.SpreadsheetNotFound:
            raise Http404("No Spreadsheet found.")
        else:
            return sh_all  # googleSheet_listing

    def test_MetadataCreaterTest(self):
        list = self.list_to_choose()
        sheet_id='1mu9CVYUIi81Ntag5eIEzJEUV8RmWT_V0DCzmh9lqwAs'
        title='iah1_metadata_2016'
        trial_year=2016
        date_import=datetime.date.today()
        metadata = Metadata.objects.create_metadata(sheet_id,title,trial_year,list)
        self.assertEqual(metadata.trial, 'IAH1')
        self.assertEqual(metadata.city, 'Ames')
        self.assertEqual(metadata.note19, 'comment iah1 19')
        self.assertEqual(metadata.cardinal, '250')

    # this method with compare two lists then return a dictionary with Imported_status(T/F), Import_date, Import_data(T/F), Refresh_data(T/F)
    def get_googleSheet_list(self,list_from_google, list_from_db):
        googleSheet_listing = []

        # Add these item in the list
        for googleSheet in list_from_google:
            single_object = {'title': googleSheet.title,'id': googleSheet.id,'imported_status': 'F','imported_date': '','import_data': 'F','refresh_data': 'F'}
            googleSheet_listing.append(single_object)

        # Add them into googleSheet_listing
        # compare with list_from_db, update certain data
        for i in range(len(googleSheet_listing)):
            for google_list_from_db in list_from_db:
                if googleSheet_listing[i]['id'] == google_list_from_db.sheet_id:
                    #print 'oh yep'
                    googleSheet_listing[i]['imported_status'] = 'T'
                    googleSheet_listing[i]['imported_date'] = google_list_from_db.date_import
                    googleSheet_listing[i]['refresh_data'] = 'T'
        # print googleSheet_listing
        return googleSheet_listing



# To test the get_googleSheet_list function
    def test_get_googleSheet_list(self):
        google_list=self.google_list_to_choose()
        db_list=self.get_titles_in_db()
        list=self.get_googleSheet_list(google_list,db_list)
        self.assertEqual(list[0]['imported_status'], 'T')
        self.assertEqual(list[0]['import_data'],'T')
        self.assertEqual(list[1]['imported_status'], 'T')
        self.assertEqual(list[1]['import_data'], 'T')
        self.assertEqual(list[2]['imported_status'], 'T')
        self.assertEqual(list[2]['import_data'], 'T')

