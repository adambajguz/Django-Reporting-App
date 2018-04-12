from django.db import models
from django.contrib.auth.models import User

class Spreadsheet(models.Model):
    user = models.ForeignKey(User, unique=True)
    spreadsheet_name = models.CharField(max_length=255)
	spreadsheet_creation_date = models.DateField(default=timezone.now, editable=False)
	spreadsheet_last_modification = models.AutoDateTimeField(default=timezone.now)
    content = models.TextField()
	variable_names = models.TextField()

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
    spreadsheet = models.ForeignKey(Spreadsheet)
	x_variable = models.CharField(max_length=255)
	y_variable = models.CharField(max_length=255)
	plot_type = models.CharField(max_length=1, choices=PLOT_TYPES)

	
class Raport(models.Model):
    user = models.ForeignKey(User, unique=True)
    raport_name = models.CharField(max_length=255)
	raport_creation_date = models.DateField(default=timezone.now, editable=False)
	raport_last_modification = models.AutoDateTimeField(default=timezone.now)
	
class RaportElementText(models.Model):
	raport = models.ForeignKey(Raport)
    element_name = models.CharField(max_length=255)
	text = models.TextField()
	
class RaportElementTable(models.Model):
    TABLE_STYLE = (
		('C', 'Classic'),
        ('M', 'Modern'),
        ('O', 'Office'),
        ('A', 'Alternating'),
    )
	
	raport = models.ForeignKey(Raport)
    table_caption = models.CharField(max_length=255)
	spreadsheet = models.ForeignKey(Spreadsheet)
	column_start = models.IntegerField()
	column_end = models.IntegerField()
	row_start = models.IntegerField()
	row_end = models.IntegerField()
	style = models.CharField(max_length=1, choices=TABLE_STYLE)
    rows_columns_inverted = models.BooleanField(default=False)
	
class RaportElementPlot(models.Model):
	raport = models.ForeignKey(Raport)
    plot_caption = models.CharField(max_length=255)
	plot = models.ForeignKey(Plot)
	
class RaportElementRaport(models.Model):
	raport = models.ForeignKey(Raport)
    embedded_raport_caption = models.CharField(max_length=255)
	embedded_raport = models.ForeignKey(Raport)
	element_start = models.IntegerField()
	element_end = models.IntegerField()