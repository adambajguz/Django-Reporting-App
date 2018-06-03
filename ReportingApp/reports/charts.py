import pygal
from pygal.style import DefaultStyle
from reports.models import Column

from django.db.models import FloatField
from django.db.models.functions import Cast

class Chart():
    def __init__(self, **kwargs):
        self.data = {}

    def set_data(self, columns):
        for column in columns:
            cells = column.cells.all()
            cells_count = cells.count()
            
            self.chart.x_labels = map(str, range(1, cells_count+1))

            cells_contents = cells.values('contents').annotate(as_float=Cast('contents', FloatField()))
            cells_float = cells_contents.values_list('as_float', flat=True)

            self.chart.add(column.column_name, cells_float)

    def generate(self):
        return self.chart.render_data_uri() 

class BarChart(Chart):
    def __init__(self, **kwargs):
        self.data = {}

        self.chart = pygal.Bar(**kwargs)
        self.chart.style = DefaultStyle(tooltip_font_size = 14)
        self.chart.legend_at_bottom = True
        self.chart.legend_at_bottom_columns=3


class LineChart(Chart):
    def __init__(self, **kwargs):
        self.data = {}

        self.chart = pygal.Line(**kwargs)
        self.chart.style = DefaultStyle(tooltip_font_size = 14)
        self.chart.legend_at_bottom = True
        self.chart.legend_at_bottom_columns=3

class PieChart(Chart):
    def __init__(self, **kwargs):
        self.data = {}

        self.chart = pygal.Pie(**kwargs)
        self.chart.style = DefaultStyle(tooltip_font_size = 14)
        self.chart.legend_at_bottom_columns=3

class RadarChart(Chart):
    def __init__(self, **kwargs):
        self.data = {}

        self.chart = pygal.Radar(**kwargs)
        self.chart.style = DefaultStyle(tooltip_font_size = 14)
        self.chart.legend_at_bottom = True
        self.chart.legend_at_bottom_columns=3

class BoxChart(Chart):
    def __init__(self, **kwargs):
        self.data = {}

        self.chart = pygal.Box(**kwargs)
        self.chart.style = DefaultStyle(tooltip_font_size = 14)
        self.chart.legend_at_bottom = True
        self.chart.box_mode = "tukey"
        self.chart.legend_at_bottom_columns=3

class PyramidChart(Chart):
    def __init__(self, **kwargs):
        self.data = {}

        self.chart = pygal.Pyramid(**kwargs)
        self.chart.style = DefaultStyle(tooltip_font_size = 14)
        self.chart.legend_at_bottom = True
        self.chart.legend_at_bottom_columns=3
        self.chart.human_readable = True

def chart_pdf(request, **kwargs):
    cht_fruits = FruitPieChart(
            height = 600,
            width = 800,
            explicit_size = True,
        )
    return render(request, 'chart_test.html', context={'output': cht_fruits.generate()})


    # return PdfRender.render('chart_test.html', params={'output': cht_fruits.generate()})
