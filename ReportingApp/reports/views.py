from django.shortcuts import render
from django.http import HttpResponse

from .models import Spreadsheet

def home(request):
    num_spreadsheets=Spreadsheet.objects.all().count()
    spreadsheets=Spreadsheet.objects.all()
    return render(request, 'home.html', context={'num_spreadsheets':num_spreadsheets, 'spreadsheets':spreadsheets}, )