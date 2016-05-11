from django.test import TestCase
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from .models import Metadata
from .models import MetadataManager

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