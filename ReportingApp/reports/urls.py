from django.urls import path
from django.conf.urls import include, url
from reports import views

urlpatterns = [
    path('', views.home, name='home'),
    path(r'spreadsheets/', views.spreadsheets, name='spreadsheets'),
    url(r'^spreadsheets/(?P<id>\d+)/delete/$', views.spreadsheets_delete),
]
