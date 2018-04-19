from django.db import models
from django.contrib.auth.models import User

class Spreadsheet(models.Model):
    user = models.ForeignKey(User, unique=True)
    spreadsheet_name = models.CharField(max_length=255)
	spreadsheet_creation_date = models.DateField(default=timezone.now, editable=False)
	spreadsheet_last_modification = models.AutoDateTimeField(default=timezone.now)
    content = models.TextField()
	variable_names = models.TextField()
	
class Column(models.Model):
    spreadsheet = models.ForeignKey(Spreadsheet)
    column_name = models.CharField(max_length=255)
    data = models.TextField()

class Plot(models.Model):
    PLOT_TYPES = (
		('B', 'Bar'),
        ('L', 'Linear'),
        ('S', 'Scatter'),
        ('P', 'Pie'),
    )
	
    plot_name = models.CharField(max_length=255)
	plot_creation_date = models.DateField(default=timezone.now, editable=False)
	plot_last_modification = models.AutoDateTimeField(default=timezone.now)
	plot_type = models.CharField(max_length=1, choices=PLOT_TYPES)
	
class PlotData(models.Model):
    PLOTDATA_TYPES = (
		('D', 'DataColumn'),
        ('G', 'GroupingColumn'),
    )
	
    plot = models.ForeignKey(Plot)
	column = models.ForeignKey(Columns)
	type = models.CharField(max_length=1, choices=PLOTDATA_TYPES)

class Report(models.Model):
    user = models.ForeignKey(User, unique=True)
    report_name = models.CharField(max_length=255)
	report_creation_date = models.DateField(default=timezone.now, editable=False)
	report_last_modification = models.AutoDateTimeField(default=timezone.now)
	
class ReportElementText(models.Model):
	report = models.ForeignKey(Report)
    element_name = models.CharField(max_length=255)
	text = models.TextField()
	order = models.IntegerField()
	
class ReportElementTable(models.Model):
    TABLE_STYLE = (
		('C', 'Classic'),
        ('M', 'Modern'),
        ('O', 'Office'),
        ('A', 'Alternating'),
    )
	
	report = models.ForeignKey(Report)
    table_caption = models.CharField(max_length=255)
	style = models.CharField(max_length=1, choices=TABLE_STYLE)
    rows_columns_inverted = models.BooleanField(default=False)
	order = models.IntegerField()
	
class ReportElementTableData(models.Model):
    TABLE_STYLE = (
		('C', 'Classic'),
        ('M', 'Modern'),
        ('O', 'Office'),
        ('A', 'Alternating'),
    )
	
	report = models.ForeignKey(ReportElementTable)
	column = models.ForeignKey(Column)
	order = models.IntegerField()	
	
class ReportElementPlot(models.Model):
	report = models.ForeignKey(Report)
    plot_caption = models.CharField(max_length=255)
	plot = models.ForeignKey(Plot)
	order = models.IntegerField()
	
class ReportElementRaport(models.Model):
	report = models.ForeignKey(Report)
    embedded_raport_caption = models.CharField(max_length=255)
	embedded_raport = models.ForeignKey(Report)
	element_start = models.IntegerField()
	element_end = models.IntegerField()
	order = models.IntegerField()