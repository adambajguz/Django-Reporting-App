from django.urls import path
from django.conf.urls import include, url
from reports import views

urlpatterns = [
    path('', views.home, name='home'),
    path(r'spreadsheets/', views.spreadsheets, name='spreadsheets'),
    url(r'^spreadsheets/add/$', views.spreadsheets_add),
    url(r'^spreadsheets/(?P<id>\d+)/delete/$', views.spreadsheets_delete, name='spreadsheets_delete'),
    url(r'^spreadsheets/(?P<id>\d+)/edit/$', views.spreadsheets_edit, name='spreadsheets_edit'),
]
