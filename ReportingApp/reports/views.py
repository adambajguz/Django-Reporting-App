from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required

from .models import Spreadsheet, Column, Cell
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
    print(spreadsheets[1].last_modification_days_ago())
    return render(request, 'spreadsheets.html', context={'spreadsheets': spreadsheets, 'num_spreadsheets': num_spreadsheets}, )

@login_required
def spreadsheets_add(request):
    spreadsheets_count = len(Spreadsheet.objects.filter(user__id = request.user.id))

    new_spreadsheet = Spreadsheet.objects.create(spreadsheet_name='New Spreadsheet #' + str(spreadsheets_count + 1), user=request.user)

    for idx in range(0,4):
        col = Column.objects.create(spreadsheet=new_spreadsheet, column_name="New column #" + str(idx))
        for _ in range(0,5):
            Cell.objects.create(column=col)

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
    # Load columns from the database
    columns = Column.objects.filter(spreadsheet__id = spreadsheet.id)

    if request.method == 'POST':
        # Extract columns
        for idx, column in enumerate(columns):
            header = request.POST.get('header_C' + str(idx + 1))
            cells = request.POST.getlist('cells_C' + str(idx + 1))

            column.column_name = header
            column.save()
            test = Cell.objects.filter(column=column.id).all()
            # test.update(contents='2')

            for idx, cell in enumerate(cells):
                record = test[idx]
                # test[idx].contets = cell !!!!!!! does not work because does not :)
                record.contents = cell
                record.save(update_fields=['contents'])

        if spreadsheet_form.is_valid():
            new_data = spreadsheet_form.cleaned_data
            # Update `spreadsheet` object
            for attr, value in new_data.items():
                # print('{} = {}'.format(attr, value))
                setattr(spreadsheet, attr, value)
            spreadsheet.save()

    num_rows = 0
    rows = []
    for current_column in columns:
        cells = [cell.contents for cell in current_column.cells.all()]
        rows.append(cells)
        num_rows = max(num_rows,len(cells))

    return render(request, 'spreadsheets_edit.html', context={'spreadsheet': spreadsheet,
                                                              'spreadsheet_form': spreadsheet_form,
                                                              'columns': columns,
                                                              'num_rows': range(0,num_rows), 'rows': rows})

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
        print("======")
        print(request.POST)
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
