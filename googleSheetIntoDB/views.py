from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Metadata


# Create your views here.
def index(request):
    template= loader.get_template('googleSheetIntoDB/index.html')
    #return HttpResponse(template.render(request))
    #return HttpResponse((request))
    return render(request,'googleSheetIntoDB/index.html')