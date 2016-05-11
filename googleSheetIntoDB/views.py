from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import TemplateView, ListView, CreateView
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect


import gspread
import gspread.exceptions
from oauth2client.service_account import ServiceAccountCredentials

from .models import Metadata
from .models import Json_path
#from .models import Sheet_Already_In_DB
from .forms import PathForm

#######################################

local_json_path ='' # the whole path that user downloaded from google oauth2client https://console.developers.google.com/
# list for the titles already in db
#google_sheet_list = [] # list for the google sheet that are not in the db yet

def index(request):
    #template= loader.get_template('googleSheetIntoDB/index.html')
    ####################### get the google sheet list

    json_objects= Json_path.objects.all()
    if json_objects==[]:
        return render(request,'googleSheetIntoDB/index.html')
    else:
        context={'json_objects': json_objects}
        return render(request,'googleSheetIntoDB/index.html',context)
# Create your views here.
def data_index(request):
    #template= loader.get_template('googleSheetIntoDB/index.html')
    ####################### get the google sheet list

    google_sheet_list= list_to_choose()
    ##########################
    titles_in_db = get_titles_in_db()
    ## tried to take out the google sheet if it is already put into the django db
    trial_year=Json_path.objects.last().trial_year
    json_path=Json_path.objects.last().json_path

    context = {'trial_year': trial_year, 'json_path': json_path,'google_sheet_list':google_sheet_list,'titles_in_db':titles_in_db}
    return render(request,'googleSheetIntoDB/data_index.html',context)


# to view the detail of Metadata by primary key as id
def detailView(request, metadata_id):
    try:
        metadata = Metadata.objects.get(pk=metadata_id)
    except Metadata.DoesNotExist:
        raise Http404("Metadata does not exist")
    return render(request, 'googleSheetIntoDB/detail.html',{'metadata': metadata})

# to view the detail of google sheets which are shared by user client email:
def detail(request):
    '''try:

    except
        raise
    '''
    return render(request, 'googleSheetIntoDB/detail.html')
################################################
class Json_Path_CreateView(CreateView):
    model= Json_path
    fields=['json_path','trial_year']

########################################################### choose to put google sheet row data into Metadata table
# this method will get the google sheet id and put that into Metadata table...


def choose(request):
    # later to create a dialog to get the path_to_json
    #path_to_json = '/Users/yiweisun/Downloads/GoogleSheetTest-d112a30fe1a8.json'



    #id = get_sheet_id()
    sheet_id = request.GET['sheet_id']
    sheet_title=request.GET['sheet_title']
    google_sheet_list = list_to_choose()
    trial_year = Json_path.objects.last().trial_year
    try:
        # 1mu9CVYUIi81Ntag5eIEzJEUV8RmWT_V0DCzmh9lqwAs
        rows = row_values_open_by_key(Json_path.objects.last().json_path, sheet_id)

    except(KeyError, 'error_message'):
        #Redisplay the google sheet selection form
        return  render(request, 'googleSheetIntoDB/data_index.html',{
            'error_message': "request does not exist.",
        })
    else:
        # put the rows into Metadata table
        if Metadata.objects.filter(sheet_id=sheet_id).exists():

            context = {'path_to_json_db':Json_path.objects.last().json_path,'sheet_id':request.GET['sheet_id'],'sheet_title':request.GET['sheet_title']}
            return render(request,'googleSheetIntoDB/data_already_exist.html',context)
        else:
            metadata = Metadata.objects.create_metadata(sheet_id,sheet_title,trial_year,rows)
        # successful put the row into db display html, display a dialog frame or
        # titles_in_db.append(title)
        # update sheet_title from data base table Metadata
            sheet_title= Metadata.objects.last()

            context = {'sheet_title': sheet_title.title, 'google_sheet_list': google_sheet_list}
            return render(request,'googleSheetIntoDB/data_in_db_success.html',context)
#######################################################################################
def choose_to_overwrite(request):
    if request.GET:
        if'_cancel' in request.GET:

            return HttpResponseRedirect('data_index.html')
    # delete the row record using DELETE FROM table_name WHERE some_column=some_value;

        elif '_yes' in request.GET:
            id = request.GET['sheet_id']
            title = request.GET['sheet_title']

            trial_year = Json_path.objects.last().trial_year
            Metadata.objects.filter(sheet_id=id).delete()

    # create a new record object with certain parameter..

            rows = row_values_open_by_key(Json_path.objects.last().json_path, id)
            metadata = Metadata.objects.create_metadata(id, title, trial_year, rows)

            sheet_title = Metadata.objects.last()
            context = {'sheet_title': sheet_title}
            return HttpResponseRedirect('data_in_db_success.html',context)


 #####################################################################################

def choose_to_input_data(request):
    if request.GET:
        if '_cancel' in request.GET:
            return HttpResponseRedirect('data_index.html')
                    # delete the row record using DELETE FROM table_name WHERE some_column=some_value;

        elif '_yes' in request.GET:
            trial_year = request.GET['trial_year']
            json_path = request.GET['json_path']
            # add an exception if there is also same object in the table so that it will not jump out the UNIQUE violation
            if Json_path.objects.filter(trial_year=trial_year, json_path=json_path).exists():
                objects = Json_path.objects.all()
                already_there= "The json path and year are already in the table."
                context={'json_objects':objects,'json_path_year_is_there':already_there}
                return render(request,'googleSheetIntoDB/index.html',context)
            else:
                json_file_path = Json_path.objects.create_json_path(json_path,trial_year)
                trial_year=Json_path.objects.last().trial_year
                json_path =Json_path.objects.last().json_path
                # create a new record object with certain parameter..

                context = {'trial_year': trial_year, 'json_path':json_path}

                return render(request,'googleSheetIntoDB/json_year_success.html', context)



#######################################################################################




def data_in_db_success(request):
    context={'sheet_title':Metadata.objects.last().title}
    return render(request, 'googleSheetIntoDB/data_in_db_success.html',context)

#######################################################################################
def data_already_exist(request):

    sheet_title=request.GET['sheet_title']
    id=request.GET['sheet_id']
    context = {'path_to_json_db': Json_path.objects.last().json_path,'sheet_already_title':sheet_title,'sheet_already_id':id}
    return render(request, 'googleSheetIntoDB/data_already_exist.html',context)

########################################################################################
def toc(request):
    google_sheet_list = list_to_choose()
    ##########################

    context = {'google_sheet_list': google_sheet_list}
    return render(request, 'googleSheetIntoDB/toc.html', context)

def detail_view(request):
    google_sheet_list = list_to_choose()

    context = {'google_sheet_list': google_sheet_list, 'sheet_title':request.GET['title'], 'sheet_id':request.GET['id']}
    return render(request, 'googleSheetIntoDB/detail_view.html',context)


##########################
def index_google_sheet_list(request):
    google_sheet_list = list_to_choose()


    context = {'google_sheet_list': google_sheet_list}
    return render(request, 'googleSheetIntoDB/index_google_sheet_list.html', context)
########################## PATH FORM  to get the json file path from a form

def get_path(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PathForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PathForm()

    return render(request, 'path.html', {'form': form})

####################################################

def list_to_choose():

    googleSheet_listing = []
    try:
        scope = ['https://spreadsheets.google.com/feeds']
       # credentials = ServiceAccountCredentials.from_json_keyfile_name('/Users/yiweisun/Downloads/GoogleSheetTest-d112a30fe1a8.json', scope)
        json_path = Json_path.objects.last().json_path
        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
        gc = gspread.authorize(credentials)
        '''
        sh = gc.open_by_id(
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
      '''
        sh_all = gc.openall()

    except gspread.exceptions.SpreadsheetNotFound:
        raise Http404("No Spreadsheet found.")
    else:
        return sh_all   #googleSheet_listing


# method to get google sheet by path_to_json and key
# path_to_json : '/Users/yiweisun/Downloads/GoogleSheetTest-d112a30fe1a8.json'
def row_values_open_by_key(path_to_json, key):
    try:
    #googleSheet_listing = []
        # '/Users/yiweisun/Downloads/GoogleSheetTest-d112a30fe1a8.json'
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(path_to_json, scope)
        gc = gspread.authorize(credentials)
        sh = gc.open_by_key(key)
    except gspread.exceptions.SpreadsheetNotFound:
        print "key is: "+ key
        raise Http404("Spreadsheet does not exist")
    else:
        worksheet = sh.get_worksheet(4)
        values_list_2 = worksheet.row_values(2)
        set_title_values(values_list_2)
        values_list_3 = worksheet.row_values(3) #the contents in row number 3

        return values_list_3


#####sh########## TITLE_VALUES ##########
def set_title_values(pass_title_values):
    global sheet_title
    sheet_title= pass_title_values

def get_title_values():
    return sheet_title
######### SHEET_ID ####################
def set_sheet_id(pass_sheet_id):
    global sheet_id
    sheet_id = pass_sheet_id
def get_sheet_id():
    return sheet_id
########### JSON_PATH #################

def set_local_json_path(local_path):
    global local_json_path # the whole path that user downloaded from google oauth2client https://console.developers.google.com/
    local_json_path = local_path


def get_local_json_path():
    return local_json_path

def get_titles_in_db():
    return Metadata.objects.all()