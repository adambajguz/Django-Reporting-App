from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.urls import reverse

from reports.models import Spreadsheet, Column, Cell
from reports.forms import SpreadsheetForm

from reports.utils.PdfRender import PdfRender

from django.contrib import messages


@login_required
def spreadsheets(request):
    # Filter spreadsheets by currenly logon user
    spreadsheets = Spreadsheet.objects.filter(user__id = request.user.id)
    num_spreadsheets = spreadsheets.count()

    return render(request, 'spreadsheets.html', context={'spreadsheets': spreadsheets, 'num_spreadsheets': num_spreadsheets}, )

@login_required
def spreadsheets_add(request):
    new_spreadsheet = Spreadsheet.create(request.user)

    return redirect('spreadsheets_edit', id=new_spreadsheet.id)

@login_required
def spreadsheets_edit(request, **kwargs):
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
        if spreadsheet_form.is_valid():
            new_data = spreadsheet_form.cleaned_data

        if request.POST.get('delete'):
            return redirect('spreadsheets_delete', id=spreadsheet_id)

        # Extract columns
        for idx, column in enumerate(columns):
            header = request.POST.get('header_C' + str(idx + 1))
            cells = request.POST.getlist('cells_C' + str(idx + 1))

            # Check if column name was updeated (speeds up saving about 10 times)
            if column.column_name != header:
                column.column_name = header
                column.save()
            database_cells = Cell.objects.filter(column=column.id)


            with transaction.atomic():
                for jdx, cell in enumerate(cells):
                    record = database_cells[jdx]
                    # database_cells[idx].contets = cell !!!!!!! does not work because does not :)

                    # Check if contents was updated (speeds up saving about 10 times)
                    if record.contents != cell:
                        record.contents = cell
                        record.save(update_fields=['contents'])

        # And notify our users that it worked
        messages.success(request, '<i class="uk-icon-floppy-o"></i> Spreadsheet saved!', extra_tags='safe')

        # Update `spreadsheet` object
        for attr, value in new_data.items():
            # print('{} = {}'.format(attr, value))
            setattr(spreadsheet_to_edit, attr, value)
        spreadsheet_to_edit.save()

        if request.POST.get('add_row'):
            #Add new cells
            new_cells_list = []
            for current_column in columns:
                new_cells_list.append(Cell(column=current_column))

            Cell.objects.bulk_create(new_cells_list)

            spreadsheet_to_edit.row_number = spreadsheet_to_edit.row_number + 1
            spreadsheet_to_edit.save()
            
            # And notify our users that it worked
            messages.warning(request, '<i class="uk-icon-arrows-v"></i> Row inserted!', extra_tags='safe')
        elif request.POST.get('add_column'):
            #Add new column
            Column.add_column(spreadsheet_to_edit)

            #Reload columns since we added one new
            columns = Column.objects.filter(spreadsheet__id = spreadsheet_to_edit.id)

            # And notify our users that it worked
            messages.warning(request, '<i class="uk-icon-arrows-h"></i> Column inserted!', extra_tags='safe')

    rows = []
    for current_column in columns:
        cells = current_column.cells.all()
        rows.append(cells.values_list('contents', flat=True))

    return render(request, 'spreadsheets_edit.html', context={'spreadsheet': spreadsheet_to_edit,
                                                              'spreadsheet_form': spreadsheet_form,
                                                              'columns': columns,
                                                              'num_rows': range(0, spreadsheet_to_edit.row_number), 'rows': rows})

@login_required
def spreadsheets_pdf(request, **kwargs):
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

    rows = []

    for current_column in columns:
        cells = current_column.cells.all()
        rows.append(cells.values_list('contents', flat=True))


    return PdfRender.render('spreadsheets_pdf.html', params={'spreadsheet': spreadsheet_to_edit,
                                                              'columns': columns,
                                                              'num_rows': range(0, spreadsheet_to_edit.row_number), 'rows': rows})

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

    return render(request, 'delete_page.html', context={'extend': "base_spreadsheets.html",
                                                        'breadcrumb': "Delete spreadsheet",
                                                        'delete_text': "<strong>'"+ spreadsheet_to_delete.spreadsheet_name +"'</strong> spreadsheet"},)

@login_required
def spreadsheets_column_delete(request, **kwargs):
    spreadsheet_id = kwargs.get('id')
    column_id = kwargs.get('cid')

    # Get current user's spreadsheets
    spreadsheet = request.user.spreadsheet_set.all()
    # Check if the `spreadsheet_id` is correct
    try:
        source_spreadsheets = spreadsheet.get(id=spreadsheet_id)
    except:
        return render(request, 'error_page.html', context={'error_message': "No spreadsheet with id:" + str(spreadsheet_id) + " was found!"})

    # Check if the `column_id` is correct
    try:
        column_to_delete = source_spreadsheets.column_set.get(id=column_id)
    except:
        return render(request, 'error_page.html', context={'error_message': "No column with id:" + str(column_id) + 
                                                                            " was found in spreadsheet '" + source_spreadsheets.spreadsheet_name + "'!"})

    if request.method == 'POST':
        # Check if user clicked on `CANCEL`
        if request.POST.get('cancel'):
            # Go back to spreadsheet list
            return redirect('spreadsheets_edit', id=spreadsheet_id)
        elif request.POST.get('delete'):
            # Delete spreadsheet by its ID
            column_to_delete.delete()

            # Update column number
            source_spreadsheets.column_number = source_spreadsheets.column_number - 1
            source_spreadsheets.save()

            # Go back to spreadsheet list
            return redirect('spreadsheets_edit', id=spreadsheet_id)

    return render(request, 'delete_page.html', context={'extend': "base_spreadsheets.html",
                                                        'breadcrumb': "<a href=\"" + reverse('spreadsheets_edit', kwargs={'id': spreadsheet_id}) 
                                                                                   + "\"\>Edit spreadsheets</a> » Delete column",
                                                        'delete_text': "<strong>'" + column_to_delete.column_name +
                                                                       "'</strong> column form <strong>'" + source_spreadsheets.spreadsheet_name +
                                                                       "'</strong> spreadsheet"},)

@login_required
def spreadsheets_row_delete(request, **kwargs):
    spreadsheet_id = kwargs.get('id')
    row_id = kwargs.get('rid')

    # Get current user's spreadsheets
    spreadsheet = request.user.spreadsheet_set.all()
    # Check if the `spreadsheet_id` is correct
    try:
        source_spreadsheets = spreadsheet.get(id=spreadsheet_id)
    except:
        return render(request, 'error_page.html', context={'error_message': "No spreadsheet with id:" + str(spreadsheet_id) + " was found!"})

   
    if request.method == 'POST':
        # Check if user clicked on `CANCEL`
        if request.POST.get('cancel'):
            # Go back to spreadsheet list
            return redirect('spreadsheets_edit', id=spreadsheet_id)
        elif request.POST.get('delete'):
            # Delete row

            # Load columns from the database
            columns = Column.objects.filter(spreadsheet__id = source_spreadsheets.id)

            row_id_int = int(row_id)
            for current_column in columns:
                cells = current_column.cells.all()
                if row_id_int >= cells.count():
                    return render(request, 'error_page.html', context={'error_message': "No row with row number:" + str(row_id) +
                                                                                        " was found in spreadsheet '" + source_spreadsheets.spreadsheet_name + "'!"})
                else:
                    # Delete cell
                    cells[row_id_int].delete()
            # Update row number
            source_spreadsheets.row_number = source_spreadsheets.row_number - 1
            source_spreadsheets.save()

            # Go back to spreadsheet list
            return redirect('spreadsheets_edit', id=spreadsheet_id)

    return render(request, 'delete_page.html', context={'extend': "base_spreadsheets.html",
                                                        'breadcrumb': "<a href=\"" + reverse('spreadsheets_edit', kwargs={'id': spreadsheet_id}) + "\"\>Edit spreadsheets</a> » Delete row",
                                                        'delete_text': "row number <strong>'" + row_id +
                                                                       "'</strong> form <strong>'" + source_spreadsheets.spreadsheet_name +
                                                                       "'</strong> spreadsheet"},)
