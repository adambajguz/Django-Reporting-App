from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from reports.models import Spreadsheet

from .forms import RegistrationForm, UserSettingsForm


def anonymous_required(view_function, redirect_to = None):
    return AnonymousRequired(view_function, redirect_to)

class AnonymousRequired(object):
    def __init__(self, view_function, redirect_to):
        if redirect_to is None:
            redirect_to = settings.LOGIN_REDIRECT_URL
        self.view_function = view_function
        self.redirect_to = redirect_to

    def __call__(self, request, *args, **kwargs):
        if request.user is not None and request.user.is_authenticated:
            return HttpResponseRedirect(self.redirect_to)
        return self.view_function(request, *args, **kwargs)

@anonymous_required
def register(request, **kwargs):
    register_form = RegistrationForm(request.POST or None,
        initial={
            'username': '',
            'email': '',
            'password': '',
            'repeat_password': '',
        }
    )
    if request.method == 'POST':
        if register_form.is_valid():
            data = register_form.cleaned_data

            # data.get('username')
            # data.get('email')
            # data.get('password')
            # data.get('repeat_password')

            # Register a new user
            username = data.get('username')
            user = User.objects.create_user(username=username,
                                 email=data.get('email'),
                                 password=data.get('password'))

            messages.add_message(request, messages.SUCCESS, username, extra_tags='username')

            # error(request, 'test')
            return redirect('login')

    return render(request, 'registration/register.html', context={'register_form': register_form})

@login_required
def profile(request):
    spreadsheets = Spreadsheet.objects.filter(user__id = request.user.id)
    num_spreadsheets = spreadsheets.count()

    return render(request, 'account/profile.html', context={'user': request.user, 'num_spreadsheets': num_spreadsheets})


@login_required
def settings(request):
    user_settings_form = UserSettingsForm(request.POST or None,
        initial={
            'username': '',
            'email': '',
            'password': '',
            'repeat_password': '',
        }
    )
    if request.method == 'POST':
        if user_settings_form.is_valid():
            data = user_settings_form.cleaned_data

            # data.get('username')
            # data.get('email')
            # data.get('password')
            # data.get('repeat_password')

            # Register a new user
            username = data.get('username')
            user = User.objects.create_user(username=username,
                                 email=data.get('email'),
                                 password=data.get('password'))

            messages.add_message(request, messages.SUCCESS, username, extra_tags='username')

            # error(request, 'test')
            return redirect('login')

    return render(request, 'account/settings.html', context={'register_form': user_settings_form})

