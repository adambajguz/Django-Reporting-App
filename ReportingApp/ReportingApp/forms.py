from django import forms

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(max_length=32, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    repeat_password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}))
