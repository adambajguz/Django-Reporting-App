from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User
from .forms import RegistrationForm
from django.contrib import messages

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
