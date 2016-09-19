from django.db import models
from django.forms import ModelForm

import datetime
# Create your models here.
# Add certain column names for the database:
# As tutorial suggests, use the Manager class to create the metadata object.
class MetadataManager(models.Manager):

    # use a list as parameter to create a metadata object
    def create_metadata(self, sheet_id,title, trial_year,list_of_values):

        metadata = self.create(sheet_id=sheet_id,title=title,trial_year= trial_year, trial = list_of_values[0], treatment=list_of_values[1],city=list_of_values[2],farm=list_of_values[3],field=list_of_values[4],trial_ID=list_of_values[5],soil=list_of_values[6],stationID=list_of_values[7],lat=list_of_values[8],long=list_of_values[9],stn_in=list_of_values[10],stn_out=list_of_values[11],prev_crop=list_of_values[12],tillage=list_of_values[13],season_tillage=list_of_values[14],plot_len=list_of_values[15],alley_Len=list_of_values[16],row_Spacing=list_of_values[17],planter=list_of_values[18],kernels_per_Plot=list_of_values[19],grain_moisture=list_of_values[20],sample_Size=list_of_values[21],LL_lat=list_of_values[22],LL_long=list_of_values[23],LR_lat=list_of_values[24],LR_long=list_of_values[25],UR_lat=list_of_values[26],UR_long=list_of_values[27],UL_lat=list_of_values[28],UL_long=list_of_values[29],cardinal=list_of_values[30],chk1_ped=list_of_values[31],chk1_src=list_of_values[32],chk2_ped=list_of_values[33],chk2_src=list_of_values[34],chk3_ped=list_of_values[35],chk3_src=list_of_values[36],chk4_ped=list_of_values[37],chk4_src=list_of_values[38],chk5_ped=list_of_values[39],chk5_src=list_of_values[40],note1=list_of_values[41],note2=list_of_values[42],note3=list_of_values[43],note4=list_of_values[44],note5=list_of_values[45],note6=list_of_values[46],note7=list_of_values[47],note8=list_of_values[48],note9=list_of_values[49],note10=list_of_values[50],note11=list_of_values[51],note12=list_of_values[52],note13=list_of_values[53],note14=list_of_values[54],note15=list_of_values[55],note16=list_of_values[56],note17=list_of_values[57],note18=list_of_values[58],note19=list_of_values[59],note20=list_of_values[60])
            # do something with the book

        return metadata

class Metadata(models.Model):
    #1
    sheet_id=models.CharField(max_length=100,unique=True,default='1ZPIYJtaPNIEpT_rvvR3WfKvXYx1_p2vZtHycCPUUaJg')
    title = models.CharField(max_length=100,default='gah1_metadata_2016') # the google sheet title
    trial_year= models.IntegerField(default=2016)  # the year that the trial happened
    date_import = models.DateField(default=datetime.date.today)  # the date that the google sheet data import to the django table
    trial = models.CharField(max_length=100)
    treatment = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    farm = models.CharField(max_length=100)
    field = models.CharField(max_length=100)
    trial_ID = models.CharField(max_length=100)
    soil = models.CharField(max_length=100)
    stationID = models.CharField(max_length=100)
    lat = models.CharField(max_length=100)
    long = models.CharField(max_length=100)

    #11
    stn_in = models.CharField(max_length=20)
    stn_out = models.CharField(max_length=20)
    prev_crop = models.CharField(max_length=100)
    tillage = models.CharField(max_length=100)
    season_tillage = models.CharField(max_length=100)
    plot_len = models.CharField(max_length=100)
    alley_Len = models.CharField(max_length=100)
    row_Spacing = models.CharField(max_length=100)
    planter = models.CharField(max_length=100)
    kernels_per_Plot = models.CharField(max_length=100)

    #21
    grain_moisture = models.CharField(max_length=100)
    sample_Size = models.CharField(max_length=100)
    LL_lat = models.CharField(max_length=100)
    LL_long = models.CharField(max_length=100)
    LR_lat = models.CharField(max_length=100)
    LR_long = models.CharField(max_length=100)

    # AA starts
    UR_lat = models.CharField(max_length=100)
    UR_long = models.CharField(max_length=100)
    UL_lat = models.CharField(max_length=100)
    UL_long = models.CharField(max_length=100)


    # 31
    cardinal = models.CharField(max_length=100)
    chk1_ped = models.CharField(max_length=100)
    chk1_src = models.CharField(max_length=100)
    chk2_ped = models.CharField(max_length=100)
    chk2_src = models.CharField(max_length=100)
    chk3_ped = models.CharField(max_length=100)
    chk3_src = models.CharField(max_length=100)
    chk4_ped = models.CharField(max_length=100)
    chk4_src = models.CharField(max_length=100)
    chk5_ped = models.CharField(max_length=100)
    # 40
    chk5_src = models.CharField(max_length=100)
    note1 = models.TextField()
    note2 = models.TextField()
    note3 = models.TextField()
    note4 = models.TextField()
    note5 = models.TextField()
    note6 = models.TextField()
    note7 = models.TextField()
    note8 = models.TextField()
    note9 = models.TextField()
    #50
    note10 = models.TextField()
    note11 = models.TextField()
    note12 = models.TextField()
    note13 = models.TextField()
    note14 = models.TextField()
    note15 = models.TextField()
    note16 = models.TextField()
    note17 = models.TextField()
    note18 = models.TextField()
    note19 = models.TextField()

    #60
    note20 = models.TextField()


    def __str__(self):  # __unicode__ on Python 2
        return self.title

    objects = MetadataManager()



 # how to create an object: example
#metadata = Metadata.objects.create_metadata("Pride and Prejudice")


########### let us use a list to modify the google sheet list as backup method.
class Json_path_Manager(models.Manager):
    def create_json_path(self, json_path, trial_year):
        json_path = self.create(json_path=json_path,trial_year=trial_year)
        return  json_path


class Json_path(models.Model):

    json_path = models.CharField(max_length=200,default='/Users/yiweisun/Downloads/GoogleSheetTest-d112a30fe1a8.json')
    trial_year = models.IntegerField(default=2016)  # the year that the trial happened

    def __str__(self):
        return self.json_path
    def get_json_path(self):
        return self.json_path

    class Meta:
        unique_together = ("json_path", "trial_year")

    objects = Json_path_Manager()

#####################################################################################
class Agronomic_Information_Manager(models.Manager):
    def create_agronomic_information(self, title,list_of_values):
      #  agronomic_information=self.create(IDsheet=id,title=title,trial=list_of_values[0],recordID=list_of_values[1],application_or_treatment=list_of_values[2],product_or_nutrient_applied=list_of_values[3],date_of_application=list_of_values[4],quantity_per_acre=list_of_values[5],application_unit=list_of_values[6])

        agronomic_information=self.create(title=title,trial=list_of_values[0],recordID=list_of_values[1],application_or_treatment=list_of_values[2],product_or_nutrient_applied=list_of_values[3],date_of_application=list_of_values[4],quantity_per_acre=list_of_values[5],application_unit=list_of_values[6])
        return agronomic_information



class Agronomic_Information(models.Model):
   # IDsheet= models.CharField(max_length=100, unique=False, default='1ZPIYJtaPNIEpT_rvvR3WfKvXYx1_p2vZtHycCPUUaJg',null=True)
    title=models.CharField(max_length=200, default='GAH1_Agronomic_Information')
    trial=models.CharField(max_length=20,null=True, default='GAH1')
    recordID=models.IntegerField(null=True, default=1)
    application_or_treatment=models.CharField(max_length=200,null=True)
    product_or_nutrient_applied=models.CharField(max_length=200,null=True)
    date_of_application=models.CharField(max_length=50,null=True)
    quantity_per_acre = models.CharField(max_length=200,null=True)
    application_unit = models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.title
    def get_recordID(self):
        return self.recordID

    objects=Agronomic_Information_Manager()

class Sheet_List(models.Model):

    title = models.CharField(max_length=200)
    json_path_id = models.ForeignKey(Json_path)
    sheet_id = models.CharField(max_length=100,unique=True)
    selected_import_list=[]
    selected_refresh_list=[]
    def __str__(self):

        return self.title

    class Meta:

        ordering = ['title']

    class Admin:

        pass
    # for template language usage
    def selected_import_list_append(self,googlesheet):
        self.selected_import_list.append(googlesheet)

    def get_seleceted_import_list(self):
        return self.selected_import_list
    def clean_selected_import_list(self):
        del self.selected_import_list[:]


    def selected_refresh_list_append(self, googlesheet):
        self.selected_refresh_list.append(googlesheet)

    def get_selected_refresh_list(self):
        return self.selected_refresh_list

    def clean_selected_refresh_list(self):
        del self.selected_refresh_list[:]

######################

## using the modelForm to get field name from model
class TitleForm(ModelForm):
    class Meta:
        model = Metadata
        fields = ['title']

