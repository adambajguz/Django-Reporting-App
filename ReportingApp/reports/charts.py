import pygal
from pygal.style import DefaultStyle
from reports.models import Column

from django.db.models import FloatField
from django.db.models.functions import Cast

class BarChart():

    def __init__(self, **kwargs):
        self.data = {}

        self.chart = pygal.Bar(**kwargs)
        self.chart.style = DefaultStyle(tooltip_font_size = 14)
        self.chart.legend_at_bottom=True

    def set_data(self, columns):
        for column in columns:
            cells = column.cells.all()
            cells_count = cells.count()
            
            self.chart.x_labels = map(str, range(1, cells_count+1))

            cells_contents = cells.values('contents').annotate(as_float=Cast('contents', FloatField()))
            cells_float = cells_contents.values_list('as_float', flat=True)

            self.chart.add(column.column_name, cells_float)

    def generate(self):
        # # Get chart data
        # chart_data = self.get_data()

        # # Add data to chart
        # for key, value in chart_data.items():
        #     self.chart.add(key, value)

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
