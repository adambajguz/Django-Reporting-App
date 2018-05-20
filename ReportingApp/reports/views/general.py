from django.shortcuts import render

from reports.models import Spreadsheet, Column, Cell

def home(request):
    spreadsheets = Spreadsheet.objects.all()
    num_spreadsheets = len(spreadsheets)
    return render(request, 'home.html', context={'spreadsheets': spreadsheets, 'num_spreadsheets': num_spreadsheets}, )

