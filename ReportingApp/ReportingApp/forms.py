from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

class RegistrationForm(forms.Form):
    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=150,
                                label=mark_safe('<i class="uk-icon-user"></i> Username'),
                                help_text="Username can contain only letters, numbers and @/./+/-/_ characters.",
                                error_messages={'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters."},
                                widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': "uk-width-1-1"}))

    email = forms.EmailField(max_length=150,
                             label=mark_safe('<i class="uk-icon-envelope"></i> e-mail'),
                             widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': "uk-width-1-1"}))

    password = forms.CharField(max_length=150,
                               label=mark_safe('<i class="uk-icon-unlock"></i> Password'),
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': "uk-width-1-1"}))

    repeat_password = forms.CharField(max_length=150,
                                      label=mark_safe('<i class="uk-icon-unlock"></i> Repeat password'),
                                      widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password', 'class': "uk-width-1-1"}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already in use.")
        return email

    def clean(self):
        form_data = self.cleaned_data
        if form_data['password'] != form_data['repeat_password']:
            self.add_error('repeat_password', "Password does not match")
            # raise ValidationError("Passwords does not match")
        return form_data