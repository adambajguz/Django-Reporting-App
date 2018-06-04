"""ReportingApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
    # from django.contrib.auth.decorators import user_passes_test
    # from django.contrib.auth.decorators import login_required
    # login_forbidden = user_passes_test(lambda u: u.is_anonymous(), '/')


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', include('reports.urls'), name='reports'),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'),

    path('accounts/settings/', views.settings, name='settings'),
    path('accounts/profile/', views.profile, name='profile'),

    url(r'^accounts/login/$', auth_views.LoginView.as_view(redirect_authenticated_user = True), name="login"),
    # url('accounts/login/', login_forbidden(auth_views.LoginView.as_view()), name='login'),
    # path('accounts/login/', views.login, name='login'),
    path('accounts/logout/', auth_views.logout_then_login, name='logout'),

    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
