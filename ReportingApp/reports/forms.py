from django import forms

class SpreadsheetForm(forms.Form):
    spreadsheet_name = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'placeholder': 'Spreadsheet name'}))
    spreadsheet_description = forms.CharField (required=False, widget=forms.Textarea(attrs={'placeholder': 'Spreadsheet description', 'rows':4}))
