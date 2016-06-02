from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import TemplateView, ListView, CreateView
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect

import datetime
import json
import ast
import string
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
    google_sheet=list_to_choose()
    titles_in_db = get_titles_in_db()
    google_sheet_list= get_googleSheet_list(google_sheet,titles_in_db)
    ##########################

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

    set_import_sheet_titles()
    #get the titles from google_sheet_list
    google_sheet_list=[]
    for sheet_list in list_to_choose():
        google_sheet_list.append(sheet_list.title)
    #id = get_sheet_id()
    for each_id in request.POST.getlist('import_checks'):
        sheet_id = each_id
        sheet_title=get_title_by_key(each_id)

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
                context = {'path_to_json_db':Json_path.objects.last().json_path,'sheet_id':sheet_id,'sheet_title':sheet_title}
                return render(request,'googleSheetIntoDB/data_already_exist.html',context)
            else:
                metadata = Metadata.objects.create_metadata(sheet_id,sheet_title,trial_year,rows)
            # successful put the row into db display html, display a dialog frame or
            # titles_in_db.append(title)
            # update sheet_title from data base table Metadata

                add_import_title(Metadata.objects.last())
    context = {'import_titles': get_import_sheet_titles(), 'google_sheet_list': google_sheet_list, 'trial_year':Json_path.objects.last().trial_year}
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
# This method will use a list from data_index.html to refresh existing Metadata object.
def choose_to_refresh(request):
    if request.POST:

        set_refresh_sheet_titles()

        refresh_list=request.POST.getlist('refresh_checks')
        import_list=request.POST.getlist('import_checks')

        # two directions: if import_data then do import data task:
        if 'import_data' in request.POST['sheet']:
            set_import_sheet_titles()
            set_refresh_sheet_titles()
            #import_data(request,request.POST.getlist('import_checks'))
            #if import_list is not empty
            if len(import_list)!=0:
                for each_id in request.POST.getlist('import_checks'):
                    sheet_id = each_id
                    sheet_title = get_title_by_key(each_id)
                    google_sheet_list = list_to_choose()
                    trial_year = Json_path.objects.last().trial_year
                    try:
                        # 1mu9CVYUIi81Ntag5eIEzJEUV8RmWT_V0DCzmh9lqwAs
                        rows = row_values_open_by_key(Json_path.objects.last().json_path, sheet_id)

                    except(KeyError, 'error_message'):
                        # Redisplay the google sheet selection form
                        return render(request, 'googleSheetIntoDB/data_index.html', {
                            'error_message': "request does not exist.",
                        })
                    else:
                        # put the rows into Metadata table
                        # if there is a file already in the db which should not happen
                        if Metadata.objects.filter(sheet_id=sheet_id).exists():

                            add_refresh_title(sheet_title)
                        else:
                            metadata = Metadata.objects.create_metadata(sheet_id, sheet_title, trial_year, rows)
                            # successful put the row into db display html, display a dialog frame or
                            # titles_in_db.append(title)
                            # update sheet_title from data base table Metadata
                            add_import_title(Metadata.objects.last().title)

                context = {'import_list': get_import_sheet_titles(),'trial_year': Json_path.objects.last().trial_year, 'org_import_list':request.POST.getlist('import_checks'),'sheet_id':sheet_id}
                return render(request, 'googleSheetIntoDB/data_in_db_success.html', context)
            elif len(import_list)==0:
                google_sheet = list_to_choose()
                titles_in_db = get_titles_in_db()
                google_sheet_list = get_googleSheet_list(google_sheet, titles_in_db)
                ##########################

                ## tried to take out the google sheet if it is already put into the django db
                trial_year = Json_path.objects.last().trial_year
                json_path = Json_path.objects.last().json_path
                context = {'google_sheet_list': google_sheet_list, 'titles_in_db': titles_in_db}
                return render(request,'googleSheetIntoDB/data_index.html',context)
    # if refresh_data, then do refresh data task:
        elif 'refresh_data' in request.POST['sheet']:
            #if refresh_list is not empty
            if refresh_list:
                for id in refresh_list:
                        #sheet_id='1mu9CVYUIi81Ntag5eIEzJEUV8RmWT_V0DCzmh9lqwAs'
                    sheet_id=id
                    title = get_title_by_key(sheet_id)
                    trial_year = Json_path.objects.last().trial_year
                    #delete the object which is already in the Metadata db
                    Metadata.objects.filter(sheet_id=id).delete()
                    # create a new record object with certain parameter..
                    rows = row_values_open_by_key(Json_path.objects.last().json_path, id)
                    metadata = Metadata.objects.create_metadata(id, title, trial_year, rows)
                    add_refresh_title(Metadata.objects.last().title)

                context = {'refresh_list':get_refresh_sheet_titles(), 'trial_year':Json_path.objects.last().trial_year}
                return render(request,'googleSheetIntoDB/refresh_data_in_db_success.html',context)
            else:
                google_sheet = list_to_choose()
                titles_in_db = get_titles_in_db()
                google_sheet_list = get_googleSheet_list(google_sheet, titles_in_db)
                ##########################

                ## tried to take out the google sheet if it is already put into the django db
                trial_year = Json_path.objects.last().trial_year
                json_path = Json_path.objects.last().json_path
                context = {'google_sheet_list': google_sheet_list,'titles_in_db':titles_in_db}
                return render(request, 'googleSheetIntoDB/data_index.html', context)
        #to delete data in the django db
        elif 'delete_data' in request.POST['sheet']:
            #get the list from delete_checks
            delete_list = request.POST.getlist('delete_checks')
            if delete_list:
                for one_delete_list in delete_list:
                    Metadata.objects.filter(sheet_id=one_delete_list).delete()
                google_sheet = list_to_choose()
                titles_in_db = get_titles_in_db()
                google_sheet_list = get_googleSheet_list(google_sheet, titles_in_db)
                context={'google_sheet_list': google_sheet_list,'titles_in_db':titles_in_db,'delete_list':delete_list,'trial_year':Json_path.objects.last().trial_year}
                return render(request,'googleSheetIntoDB/refresh_data_in_db_success.html',context)
            else:


                google_sheet = list_to_choose()
                titles_in_db = get_titles_in_db()
                google_sheet_list = get_googleSheet_list(google_sheet, titles_in_db)
                ##########################

                ## tried to take out the google sheet if it is already put into the django db
                trial_year = Json_path.objects.last().trial_year
                json_path = Json_path.objects.last().json_path
                context = {'google_sheet_list': google_sheet_list, 'titles_in_db': titles_in_db}
                return render(request, 'googleSheetIntoDB/data_index.html', context)

        else:
            return render(request,'googleSheetIntoDB/no_list_to_select.html')
    else:
        return render(request,'googleSheetIntoDB/no_list_to_select.html')
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

def refresh_data_in_db_success(request):
    context={'sheet_title':Metadata.objects.last().title, 'refresh_titles':get_refresh_sheet_titles()}
    return render(request, 'googleSheetIntoDB/refresh_data_in_db_success.html',context)


def data_in_db_success(request):
    context={'sheet_title':Metadata.objects.last().title, 'refresh_titles':get_refresh_sheet_titles()}
    return render(request, 'googleSheetIntoDB/data_in_db_success.html',context)
#######################################################################################
def data_already_exist(request):

    sheet_title=request.GET['sheet_title']
    id=request.GET['sheet_id']
    context = {'path_to_json_db': Json_path.objects.last().json_path,'sheet_already_title':sheet_title,'sheet_already_id':id}
    return render(request, 'googleSheetIntoDB/data_already_exist.html',context)


def no_list_to_select(request):
    context={}
    return render(request,'googleSheetIntoDB/no_list_to_select.html',context)
########################################################################################

def detail_view(request):
    google_sheet_list = list_to_choose()
    context = {'google_sheet_list': google_sheet_list, 'sheet_id':request.GET['detail_id'],'title':request.GET['detail_title']}
    return render(request, 'googleSheetIntoDB/detail_view.html',context)


#########################################################################################
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
    try:
        scope = ['https://spreadsheets.google.com/feeds']
       # credentials = ServiceAccountCredentials.from_json_keyfile_name('/Users/yiweisun/Downloads/GoogleSheetTest-d112a30fe1a8.json', scope)
        json_path = Json_path.objects.last().json_path
        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
        gc = gspread.authorize(credentials)
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
        #worksheet = sh.get_worksheet(4)
        worksheet=sh.worksheet('data_collector')
        values_list_2 = worksheet.row_values(2)
        set_title_values(values_list_2)
        values_list_3 = worksheet.row_values(3) #the contents in row number 3

        return values_list_3
####################################################################################################
def get_title_by_key(key):
    try:
        # googleSheet_listing = []
        # '/Users/yiweisun/Downloads/GoogleSheetTest-d112a30fe1a8.json'
        scope = ['https://spreadsheets.google.com/feeds']
        #json_path = Json_path.objects.last().json_path
        json_path ='/Users/yiweisun/Downloads/GoogleSheetTest-d112a30fe1a8.json'
        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
        gc = gspread.authorize(credentials)
        sh = gc.open_by_key(key)
    except gspread.exceptions.SpreadsheetNotFound:
        print "key is: " + key
        raise Http404("Spreadsheet does not exist")
    else:
        return sh.title

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
##########################################################################################################################################
#  IMPORTANT FOR DATA_INDEX.HTML
#########################################################################################################################################
# this method with compare two lists then return a dictionary with Imported_status(T/F), Import_date, Import_data(T/F), Refresh_data(T/F)
def get_googleSheet_list(list_from_google, list_from_db):
    googleSheet_listing = []

    # Add these item in the list
    for googleSheet in list_from_google:
        single_object={'title':googleSheet.title, 'id':googleSheet.id,'imported_status':'F','imported_date': '','import_data': 'T','refresh_data': 'F'}
        googleSheet_listing.append(single_object)

    # Add them into googleSheet_listing
    # compare with list_from_db, update certain data
    for i in range(len(googleSheet_listing)):
        for google_list_from_db in list_from_db:
            if googleSheet_listing[i]['id'] == google_list_from_db.sheet_id:
                    googleSheet_listing[i]['imported_status']='T'
                    googleSheet_listing[i]['imported_date']=google_list_from_db.date_import
                    googleSheet_listing[i]['import_data'] = 'F'
                    googleSheet_listing[i]['refresh_data']='T'
    return googleSheet_listing
##############################################################################################################################################
def get_titles_in_db():
    return Metadata.objects.all()

def get_year_from_row_values(row_values):
    try:

        trial_year=row_values[10]
        trial_year=trial_year.split('/')[2]
    except trial_year:
        raise ('trial_year is empty.')
    else:
        return trial_year
#################################################################################
def set_refresh_sheet_titles():
    global refresh_sheet_titles
    refresh_sheet_titles=[]


def add_refresh_title(title):

    refresh_sheet_titles.append(str(title))

def get_refresh_sheet_titles():
    return refresh_sheet_titles

def clean_refresh_sheet_titles():
    refresh_sheet_titles.clean()

##################################################################################
def set_import_sheet_titles():
    global import_sheet_titles
    import_sheet_titles=[]

def add_import_title(title):
    import_sheet_titles.append(str(title))

def get_import_sheet_titles():
    return import_sheet_titles

def clean_import_sheet_titles():
    import_sheet_titles.clean()
####################################################################################

def import_data(request,list):
    for each_id in list:
        sheet_id = each_id
        sheet_title = get_title_by_key(each_id)
        google_sheet_list = list_to_choose()
        trial_year = Json_path.objects.last().trial_year
        try:
            # 1mu9CVYUIi81Ntag5eIEzJEUV8RmWT_V0DCzmh9lqwAs
            rows = row_values_open_by_key(Json_path.objects.last().json_path, sheet_id)

        except(KeyError, 'error_message'):
            # Redisplay the google sheet selection form
            return render(request, 'googleSheetIntoDB/data_index.html', {
                'error_message': "request does not exist.",
            })
        else:
            # put the rows into Metadata table
            # if there is a file already in the db which should not happen
            if Metadata.objects.filter(sheet_id=sheet_id).exists():

                add_refresh_title(sheet_title)
            else:
                metadata = Metadata.objects.create_metadata(sheet_id, sheet_title, trial_year, rows)
                # successful put the row into db display html, display a dialog frame or
                # titles_in_db.append(title)
                # update sheet_title from data base table Metadata
                add_import_title(sheet_title)

    context = { 'import_list': get_import_sheet_titles(),
               'trial_year': Json_path.objects.last().trial_year}
    return render(request, 'googleSheetIntoDB/data_in_db_success.html', context)

#########################################################################################################
