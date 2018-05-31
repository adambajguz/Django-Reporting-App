import pygal
from pygal.style import DefaultStyle
from reports.models import Column

class BarChart():

    def __init__(self, **kwargs):
        self.chart = pygal.Bar(**kwargs)
        self.chart.title = 'Amount of Fruits'
        self.chart.style = DefaultStyle


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



def chart_pdf(request, **kwargs):
    cht_fruits = FruitPieChart(
            height = 600,
            width = 800,
            explicit_size = True,
        )
    return render(request, 'chart_test.html', context={'output': cht_fruits.generate()})


    # return PdfRender.render('chart_test.html', params={'output': cht_fruits.generate()})
