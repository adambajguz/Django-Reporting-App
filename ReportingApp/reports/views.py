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
    num_spreadsheets = spreadsheets.count()
    return render(request, 'spreadsheets.html', context={'spreadsheets': spreadsheets, 'num_spreadsheets': num_spreadsheets}, )

@login_required
def spreadsheets_add(request):
    # spreadsheets_count = len(Spreadsheet.objects.filter(user__id = request.user.id))

    # new_spreadsheet = Spreadsheet.objects.create(spreadsheet_name='New Spreadsheet #' + str(spreadsheets_count + 1), user=request.user)

    # for idx in range(0,4):
    #     Column.add_column(new_spreadsheet, 5)

    new_spreadsheet = Spreadsheet.create(request.user)


    return redirect('spreadsheets_edit', id=new_spreadsheet.id)


import time
from datetime import timedelta

@login_required
def spreadsheets_edit(request, **kwargs):
    start_time = time.monotonic()

    # Get id
    spreadsheet_id = kwargs.get('id')

    # Get current user's spreadsheets
    user_spreadsheets = request.user.spreadsheet_set.all()
    # Check if the `spreadsheet_id` is correct
    try:
        spreadsheet_to_edit = user_spreadsheets.get(id=spreadsheet_id)
    except:
        return render(request, 'error_page.html', context={'error_message': "No spreadsheet with id:" + str(spreadsheet_id) + " was found!"})

    spreadsheet_form = SpreadsheetForm(request.POST or None,
        initial={
            'spreadsheet_name': spreadsheet_to_edit.spreadsheet_name,
            'spreadsheet_description': spreadsheet_to_edit.spreadsheet_description,
        }
    )

    # Load columns from the database
    columns = Column.objects.filter(spreadsheet__id = spreadsheet_to_edit.id)

    if request.method == 'POST':
        # Extract columns
        print("SAVE")

        for idx, column in enumerate(columns):
            header = request.POST.get('header_C' + str(idx + 1))
            cells = request.POST.getlist('cells_C' + str(idx + 1))

            # check if column name was updeated (speeds up saving about 10 times)
            if column.column_name != header:
                column.column_name = header
                column.save()
            database_cells = Cell.objects.filter(column=column.id)

            for jdx, cell in enumerate(cells):
                record = database_cells[jdx]
                # database_cells[idx].contets = cell !!!!!!! does not work because does not :)

                # check if contents was updeated (speeds up saving about 10 times)
                if record.contents != cell:
                    record.contents = cell
                    record.save(update_fields=['contents'])

        if spreadsheet_form.is_valid():
            new_data = spreadsheet_form.cleaned_data
            # Update `spreadsheet` object
            for attr, value in new_data.items():
                # print('{} = {}'.format(attr, value))
                setattr(spreadsheet_to_edit, attr, value)
            spreadsheet_to_edit.save()

            end_time = time.monotonic()
            print(timedelta(seconds=end_time - start_time))

            if request.POST.get('add_row'):
                print("Add row")

                for current_column in columns:
                    Cell.objects.create(column=current_column)
            elif request.POST.get('add_column'):
                # Get all ids of columns in current spreadsheet
                current_columns_ids = columns.values_list('id', flat=True)
                # Calculate number of columns
                current_columns_count = current_columns_ids.count()
                # Get total number of cells in column
                current_cells_count = Cell.objects.filter(column__in = current_columns_ids).count()
                # Calculate number of cells in each column
                current_cells_in_column_count = current_cells_count // current_columns_count

                #Add new column
                Column.add_column(spreadsheet_to_edit, current_cells_in_column_count)
                Column.add_column(spreadsheet_to_edit, current_cells_in_column_count)
                Column.add_column(spreadsheet_to_edit, current_cells_in_column_count)
                Column.add_column(spreadsheet_to_edit, current_cells_in_column_count)
                Column.add_column(spreadsheet_to_edit, current_cells_in_column_count)
                Column.add_column(spreadsheet_to_edit, current_cells_in_column_count)

                #Reload columns since we added one new
                columns = Column.objects.filter(spreadsheet__id = spreadsheet_to_edit.id)

    num_rows = 0
    rows = []
    for current_column in columns:
        cells = [cell.contents for cell in current_column.cells.all()]
        rows.append(cells)
        num_rows = max(num_rows,len(cells))

    end_time = time.monotonic()
    print(timedelta(seconds=end_time - start_time)) 
    return render(request, 'spreadsheets_edit.html', context={'spreadsheet': spreadsheet_to_edit,
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
        return render(request, 'error_page.html', context={'error_message': "No spreadsheet with id:" + str(spreadsheet_id) + " was found!"})

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

    return render(request, 'spreadsheet_delete.html', context={'spreadsheet_name': spreadsheet_to_delete.spreadsheet_name},)
