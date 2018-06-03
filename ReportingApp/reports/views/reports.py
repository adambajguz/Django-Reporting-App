from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from reports.models import *

from django.forms.formsets import formset_factory
from reports.forms import ReportForm, ReportElementForm
from django.forms.formsets import BaseFormSet

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
    report_id = kwargs.get('id')

    # Get current user's reports
    user_reports = request.user.report_set.all()
    # Check if the `report_id` is correct
    try:
        report_to_edit = user_reports.get(id=report_id)
    except:
        return render(request, 'error_page.html', context={'error_message': "No report with id:" + str(report_id) + " was found!"})

    # Create the formset, specifying the form and formset we want to use
    ReportElementFormSet = formset_factory(ReportElementForm, formset=BaseFormSet)

    # Get our existing link data for this user. This is used as initial data.
    report_elements = ReportElement.objects.filter(report=report_to_edit).order_by('element_order')
    report_elements_data = report_elements.values()

    if request.method == 'POST':
        report_form = ReportForm(request.POST)
        report_element_formset= ReportElementFormSet(request.POST)

        if report_form.is_valid() and report_element_formser.is_valid():

            report_new_data = report_form.cleaned_data
            # Update `report` object
            for attr, value in report_new_data.items():
                # print('{} = {}'.format(attr, value))
                setattr(report_to_edit, attr, value)

            new_elements = []

    else:
        report_form = ReportForm(initial={
            'report_name': report_to_edit.report_name,
        })
        report_element_formset = ReportElementFormSet(initial=report_elements_data,)

    return render(request, 'reports_edit.html', context={'report': report_to_edit, 'report_form': report_form, 'report_element_formset': report_element_formset})

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
