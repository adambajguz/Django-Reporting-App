from django import forms
from .models import Plot

class SpreadsheetForm(forms.Form):
    spreadsheet_name = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'placeholder': 'Spreadsheet name'}))
    spreadsheet_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': 'Spreadsheet description', 'rows':4}))

class PlotForm(forms.Form):
    plot_name = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'placeholder': 'Plot name'}))
    plot_type = forms.ChoiceField(choices=Plot.PLOT_TYPES)
