from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Spreadsheet)
admin.site.register(Column)
admin.site.register(Cell)
admin.site.register(Plot)
admin.site.register(Report)
admin.site.register(ReportElement)
# admin.site.register(ReportElementText)
# admin.site.register(ReportElementTable)
# admin.site.register(ReportElementTableData)
# admin.site.register(ReportElementPlot)
# admin.site.register(ReportElementReport)
