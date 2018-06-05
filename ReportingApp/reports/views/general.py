from django.shortcuts import render

from reports.models import Spreadsheet, Plot, Report
from django.contrib.auth.models import User

def home(request):
    num_spreadsheets = Spreadsheet.objects.all().count()
    num_plots = Plot.objects.all().count()
    num_reports = Report.objects.all().count()

    objects_count = num_spreadsheets + num_plots + num_reports

    users_count = User.objects.all().count()
    
    return render(request, 'home.html', context={'users_count': users_count, 'objects_count': objects_count}, )

