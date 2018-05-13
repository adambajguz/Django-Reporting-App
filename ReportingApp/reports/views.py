from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required

from .models import Spreadsheet, Column
from .forms import SpreadsheetForm

import json

def home(request):
    spreadsheets = Spreadsheet.objects.all()
    num_spreadsheets = len(spreadsheets)
    return render(request, 'home.html', context={'spreadsheets': spreadsheets, 'num_spreadsheets': num_spreadsheets}, )

@login_required
def spreadsheets(request):
    # Filter spreadsheets by currenly logon user
    spreadsheets = Spreadsheet.objects.filter(user__id = request.user.id)
    num_spreadsheets = len(spreadsheets)
    return render(request, 'spreadsheets.html', context={'spreadsheets': spreadsheets, 'num_spreadsheets': num_spreadsheets}, )

@login_required
def spreadsheets_add(request):
    new_spreadsheet = Spreadsheet.objects.create(spreadsheet_name='New Spreadsheet', user=request.user)
    return redirect('spreadsheets_edit', id=new_spreadsheet.id)

@login_required
def spreadsheets_edit(request, **kwargs):
    # Get Spreadsheet
    spreadsheet = Spreadsheet.objects.get(id=kwargs.get('id'))
    spreadsheet_form = SpreadsheetForm(request.POST or None,
        initial={
            'spreadsheet_name': spreadsheet.spreadsheet_name,
        }
    )

    columns = Column.objects.filter(spreadsheet__id = spreadsheet.id)

    num_rows = 0
    c = list()
    for current_column in columns:
        c.append(current_column.data.split(";"))
        current_column.data = current_column.data.split(";")

        print("UNPACKED: ", current_column.data)
        print("REPACKED", ";".join(current_column.data))
        print("JSON PACKED: ", json.dumps(current_column.data))
        jsonDec = json.decoder.JSONDecoder()
        print("JSON UNPACKED: ", jsonDec.decode(json.dumps(current_column.data)))
        num_rows = max(num_rows,len(current_column.data))

    print(c)


    if request.method == 'POST':
        # Update `spreadsheet` object
        if spreadsheet_form.is_valid():
            new_data = spreadsheet_form.cleaned_data
            print('OLD VERISON:', spreadsheet)
            print('NEW VERISON:', new_data)
            # Update object's fields

            for attr, value in new_data.items():
                print('{} = {}'.format(attr, value))
                setattr(spreadsheet, attr, value)
            spreadsheet.save()
    
    return render(request, 'spreadsheets_edit.html', context={'spreadsheet': spreadsheet, 'spreadsheet_form': spreadsheet_form, 'columns': columns, 'rows': range(0,num_rows)}, )

@login_required
def spreadsheets_delete(request, **kwargs):
    spreadsheet_id = kwargs.get('id')

    # Get current user's spreadsheets
    spreadsheets = request.user.spreadsheet_set.all()
    # Check if the `spreadsheet_id` is correct
    try:
        spreadsheet_to_delete = spreadsheets.get(id=spreadsheet_id)
    except:
        raise Http404('No Spreadsheet found!')

    if request.method == 'POST':
        # Check if user clicked on `CANCEL`
        if request.POST.get('cancel'):
            # Go back to spreadsheet list
            return redirect('spreadsheets')
        elif request.POST.get('delete'):
            # Delete spreadsheet by its ID
            spreadsheet_to_delete.delete()
            # Go back to spreadsheet list
            return redirect('spreadsheets')

    return render(request, 'spreadsheet_delete.html', context={},)
