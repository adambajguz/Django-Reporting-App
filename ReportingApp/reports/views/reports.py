from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from reports.models import *

from django.forms.formsets import formset_factory
from reports.forms import ReportForm, ReportElementForm
from django.forms.formsets import BaseFormSet

from django.db import IntegrityError, transaction
from django.contrib import messages

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
def reports_add_element(request, **kwargs):
    report_id = kwargs.get('id')

    # Get current user's reports
    user_reports = request.user.report_set.all()
    # Check if the `report_id` is correct
    try:
        report_to_edit = user_reports.get(id=report_id)
    except:
        return render(request, 'error_page.html', context={'error_message': "No report with id:" + str(report_id) + " was found!"})

    
    ReportElement.objects.create(report = report_to_edit, element_order = report_to_edit.reportElements.count())
    
    return redirect('reports_edit', id=report_id)


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
    ReportElementFormSet = formset_factory(ReportElementForm, formset=BaseFormSet, extra=0)

    # Get our data for. This is used as initial data.
    report_elements = ReportElement.objects.filter(report=report_to_edit).order_by("element_order")
    report_elements_count = report_elements.count()

    print("==========")
    for el in report_elements:
        print(dir(el))
    print("==========")
    report_elements_data = report_elements.values()
    for el in report_elements:
        a = getattr(el, 'spreadsheet')
        print(a)

    # get ids usign values() and get queryset of object using Spreadsheet.objects.filter(id=id) 
    #x.fields["nazwa_fieldu"].initial = coś



    print("--------------")

    if request.method == 'POST':
        if request.POST.get('delete'):
            return redirect('reports_delete', id=report_id)

        report_form = ReportForm(request.POST)
        report_element_formset = ReportElementFormSet(request.POST, form_kwargs = {'user': request.user})

        if report_form.is_valid() and report_element_formset.is_valid():
            report_new_data = report_form.cleaned_data
            # Update `report` object
            for attr, value in report_new_data.items():
                # print('{} = {}'.format(attr, value))
                setattr(report_to_edit, attr, value)
            report_to_edit.save()

            # Now save the data for each form in the formset
            new_elements = []

            for form in report_element_formset:
                new_data = form.cleaned_data
                new_element = ReportElement(report=report_to_edit)

                for attr, value in new_data.items():
                    # print('{} = {}'.format(attr, value))
                    setattr(new_element, attr, value)
                new_elements.append(new_element)

            try:
                with transaction.atomic():
                    #Replace the old with the new
                    ReportElement.objects.filter(report=report_to_edit).delete()
                    ReportElement.objects.bulk_create(new_elements)

                    # And notify our users that it worked
                    messages.success(request, '<i class="uk-icon-floppy-o"></i> Report saved!', extra_tags='safe')

            except IntegrityError: #If the transaction failed
                messages.error(request, '<i class="uk-icon-ban"></i> There was an error saving your report.', extra_tags='safe')

        if request.POST.get('add'):
            return redirect('reports_add_element', id=report_id)

    else:
        report_form = ReportForm(initial={
            'report_name': report_to_edit.report_name,
            'report_description': report_to_edit.report_description,
        })

        # a = [{'plot': Plot.objects.filter(id__in=report_elements.values("plot_id"))}]
        report_element_formset = ReportElementFormSet(initial=report_elements_data, form_kwargs = {'user': request.user})
    return render(request, 'reports_edit.html', context={'report': report_to_edit, 'report_form': report_form, 'report_element_formset': report_element_formset,
                                                         'report_elements_count': report_elements_count,})


@login_required
def reports_preview(request, **kwargs):
    # Get id
    report_id = kwargs.get('id')

    # Get current user's reports
    user_reports = request.user.report_set.all()
    # Check if the `report_id` is correct
    try:
        report_to_preview = user_reports.get(id=report_id)
    except:
        return render(request, 'error_page.html', context={'error_message': "No report with id:" + str(report_id) + " was found!"})

    # Get our data for. This is used as initial data.
    report_elements = ReportElement.objects.filter(report=report_to_preview).order_by("element_order")
    report_elements_count = report_elements.count()

    for el in report_elements:
       print(el)


    return render(request, 'reports_preview.html', context={'report': report_to_preview, 'report_elements': report_elements, 'report_elements_count': report_elements_count,})
@login_required
def reports_pdf(request, **kwargs):
    return render(request, 'reports_edit.html', context={'report': report_to_edit, 'report_form': report_form, 'report_element_formset': report_element_formset,
                                                         'report_elements_count': report_elements_count,})
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


@login_required
def reports_delete_element(request, **kwargs):
    report_id = kwargs.get('id')
    element_id = kwargs.get('eid')

    # Get current user's reports
    reports = request.user.report_set.all()
    # Check if the `report_id` is correct
    try:
        source_reports = reports.get(id=report_id)
    except:
        return render(request, 'error_page.html', context={'error_message': "No report with id:" + str(report_id) + " was found!"})

    # Check if the `element_id` is correct
    try:
        report_element_to_delete = source_reports.reportElements.get(id=element_id)
    except:
        return render(request, 'error_page.html', context={'error_message': "No element with id:" + str(element_id) + 
                                                                            " was found in report '" + source_reports.report_name + "'!"})

    if request.method == 'POST':
        # Check if user clicked on `CANCEL`
        if request.POST.get('cancel'):
            # Go back to reports edit
            return redirect('reports_edit', id=report_id)
        elif request.POST.get('delete'):
            # Delete element by its ID
            report_element_to_delete.delete()

            # Go back to reports edit
            return redirect('reports_edit', id=report_id)

    return render(request, 'delete_page.html', context={'extend': "base_reports.html",
                                                        'breadcrumb': "<a href=\"" + reverse('reports_edit', kwargs={'id': report_id}) 
                                                                                   + "\"\>Edit report</a> » Delete element",
                                                        'delete_text': "<strong>'" + report_element_to_delete.element_name +
                                                                       "'</strong> element form <strong>'" + source_reports.report_name +
                                                                       "'</strong> report"},)