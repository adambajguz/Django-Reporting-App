from django.urls import path
from django.conf.urls import include, url
from reports import views

urlpatterns = [
    path('', views.home, name='home'),
    path(r'spreadsheets/', views.spreadsheets, name='spreadsheets'),
    url(r'^spreadsheets/add/$', views.spreadsheets_add),
    url(r'^spreadsheets/(?P<id>\d+)/delete/$', views.spreadsheets_delete, name='spreadsheets_delete'),
    url(r'^spreadsheets/(?P<id>\d+)/edit/$', views.spreadsheets_edit, name='spreadsheets_edit'),
    url(r'^spreadsheets/(?P<id>\d+)/pdf/$', views.spreadsheets_pdf, name='spreadsheets_pdf'),

    path(r'plots/', views.plots, name='plots'),
    url(r'^plots/add/$', views.plots_add),
    url(r'^plots/(?P<id>\d+)/delete/$', views.plots_delete, name='plots_delete'),
    url(r'^plots/(?P<id>\d+)/edit/$', views.plots_edit, name='plots_edit'),

    path(r'reports/', views.spreadsheets, name='reports'),
    path(r'chartpdf/', views.chart_pdf),
]
