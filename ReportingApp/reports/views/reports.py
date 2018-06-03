from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from reports.models import *


@login_required
def reports(request):
    # Filter reports by currenly logon user
    reports = Report.objects.filter(user__id = request.user.id)
    num_reports = reports.count()

    return render(request, 'reports.html', context={'reports': reports, 'num_reports': num_reports}, )

@login_required
def reports_add(request):
    new_report = Report.create(request.user)

    return redirect('reports_edit', id=new_report.id)


@login_required
def reports_edit(request, **kwargs):
    # Get id
    plot_id = kwargs.get('id')

    # Get current user's plots
    user_plots = request.user.plot_set.all()
    # Check if the `plot_id` is correct
    try:
        plot_to_edit = user_plots.get(id=plot_id)
    except:
        return render(request, 'error_page.html', context={'error_message': "No plot with id:" + str(plot_id) + " was found!"})

    plot_form = PlotForm(request.user, request.POST or None,
        initial={
            'plot_name': plot_to_edit.plot_name,
            'plot_type': plot_to_edit.plot_type,
            'spreadsheet': plot_to_edit.spreadsheet,
        }
    )

    if request.method == 'POST':
        if request.POST.get('delete'):
            return redirect('plots_delete', id=plot_id)

        if plot_form.is_valid():
            new_data = plot_form.cleaned_data
            # Update `plot` object
            for attr, value in new_data.items():
                # print('{} = {}'.format(attr, value))
                setattr(plot_to_edit, attr, value)


        plot_to_edit.data_columns = str(request.POST.getlist('data_col')).strip('[]').replace("'", "")
        plot_to_edit.grouping_columns = str(request.POST.getlist('grouping_col')).strip('[]').replace("'", "")

        plot_to_edit.save()

    print("Test",plot_to_edit.data_columns)

    data_columns = [int(i) for i in plot_to_edit.data_columns.replace("'", "").split(', ')]
    grouping_columns = [int(i) for i in plot_to_edit.grouping_columns.replace("'", "").split(', ')]
    # data_columns = []
    # grouping_columns = []
    actual_plot = BarChart(
            height = 600,
            width = 800,
            explicit_size = True,
            title = "Title"
        )

    columns = Column.objects.filter(spreadsheet=plot_to_edit.spreadsheet)
    actual_plot.set_data(columns.filter(id__in=data_columns))

    return render(request, 'plots_edit.html', context={'plot': plot_to_edit,
                                                       'plot_form': plot_form,
                                                       'plot_graphics': actual_plot.generate(),
                                                       'columns': columns,
                                                       'data_columns': data_columns,
                                                       'grouping_columns': grouping_columns})

@login_required
def reports_delete(request, **kwargs):
    report_id = kwargs.get('id')

    # Get current user's reports
    reports = request.user.report_set.all()
    # Check if the `report_id` is correct
    try:
        report_to_delete = reports.get(id=report_id)
    except:
        return render(request, 'error_page.html', context={'error_message': "No report with id:" + str(report_id) + " was found!"})

    if request.method == 'POST':
        # Check if user clicked on `CANCEL`
        if request.POST.get('cancel'):
            # Go back to spreadsheet list
            return redirect('reports')
        elif request.POST.get('delete'):
            # Delete spreadsheet by its ID
            report_to_delete.delete()
            # Go back to spreadsheet list
            return redirect('reports')

    return render(request, 'delete_page.html', context={'extend': "base_reports.html",
                                                        'breadcrumb': "Delete report",
                                                        'delete_text': "<strong>'"+ report_to_delete.report_name +"'</strong> report"},)
