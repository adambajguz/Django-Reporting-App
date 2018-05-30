from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction

from reports.forms import PlotForm

from reports.models import Spreadsheet, Column, Cell, Plot, PlotData

import pygal
from pygal.style import DefaultStyle


class FruitPieChart():

    def __init__(self, **kwargs):
        self.chart = pygal.Bar(**kwargs)
        self.chart.title = 'Amount of Fruits'

    def get_data(self):
        '''
        Query the db for chart data, pack them into a dict and return it.
        '''
        data = {}
        for fruit in Column.objects.all():
            data[fruit.column_name] = fruit.spreadsheet.id
        return data

    def generate(self):
        # Get chart data
        chart_data = self.get_data()

        # Add data to chart
        for key, value in chart_data.items():
            self.chart.add(key, value)

        # Return the rendered SVG
        
        return self.chart.render_data_uri() 
        #return self.chart.render(is_unicode=True, disable_xml_declaration=True)


# from .charts import FruitPieChart


def chart_pdf(request, **kwargs):
    cht_fruits = FruitPieChart(
            height=600,
            width=800,
            explicit_size=True,
            style=DefaultStyle
        )
    return render(request, 'chart_test.html', context={'output': cht_fruits.generate()})


    # return PdfRender.render('chart_test.html', params={'output': cht_fruits.generate()})



@login_required
def plots(request):
    # Filter spreadsheets by currenly logon user
    plots = Plot.objects.filter(user__id = request.user.id)
    num_plots = plots.count()

    return render(request, 'plots.html', context={'plots': plots, 'num_plots': num_plots}, )


@login_required
def plots_add(request):
    new_plot = Plot.create(request.user)

    return redirect('plots_edit', id=new_plot.id)

@login_required
def plots_edit(request, **kwargs):
    # Get id
    plot_id = kwargs.get('id')

    # Get current user's plots
    user_plots = request.user.plot_set.all()
    # Check if the `spreadsheet_id` is correct
    try:
        plot_to_edit = user_plots.get(id=plot_id)
    except:
        return render(request, 'error_page.html', context={'error_message': "No plot with id:" + str(plot_id) + " was found!"})

    plot_form = PlotForm(request.POST or None,
        initial={
            'plot_name': plot_to_edit.plot_name,
        }
    )

    actual_plot = FruitPieChart(
            height=600,
            width=800,
            explicit_size=True,
            style=DefaultStyle
        )

    if request.method == 'POST':
        if plot_form.is_valid():
            new_data = plot_form.cleaned_data

        if request.POST.get('delete'):
            return redirect('plots_delete', id=plot_id)

        # Update `plot` object
        for attr, value in new_data.items():
            # print('{} = {}'.format(attr, value))
            setattr(plot_to_edit, attr, value)
        plot_to_edit.save()


    return render(request, 'plots_edit.html', context={'plot': plot_to_edit,
                                                       'plot_form': plot_form,
                                                       'plot_graphics': actual_plot.generate(),})

@login_required
def plots_delete(request, **kwargs):
    plot_id = kwargs.get('id')

    # Get current user's plots
    plots = request.user.plot_set.all()
    # Check if the `plot_id` is correct
    try:
        plot_to_delete = plots.get(id=plot_id)
    except:
        return render(request, 'error_page.html', context={'error_message': "No plot with id:" + str(plot_id) + " was found!"})

    if request.method == 'POST':
        # Check if user clicked on `CANCEL`
        if request.POST.get('cancel'):
            # Go back to spreadsheet list
            return redirect('plots')
        elif request.POST.get('delete'):
            # Delete spreadsheet by its ID
            plot_to_delete.delete()
            # Go back to spreadsheet list
            return redirect('plots')

    return render(request, 'plot_delete.html', context={'plot_name': plot_to_delete.plot_name},)
