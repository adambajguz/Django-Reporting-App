from django.urls import path
from django.conf.urls import include, url
from reports import views

urlpatterns = [
    path('', views.home, name='home'),
    path(r'spreadsheets/', views.spreadsheets, name='spreadsheets'),
    url(r'^spreadsheets/add/$', views.spreadsheets_add, name='spreadsheets_add'),
    url(r'^spreadsheets/(?P<id>\d+)/delete/$', views.spreadsheets_delete, name='spreadsheets_delete'),
    url(r'^spreadsheets/(?P<id>\d+)/edit/$', views.spreadsheets_edit, name='spreadsheets_edit'),
    url(r'^spreadsheets/(?P<id>\d+)/pdf/$', views.spreadsheets_pdf, name='spreadsheets_pdf'),
    url(r'^spreadsheets/(?P<id>\d+)/edit/column/(?P<cid>\d+)/delete$', views.spreadsheets_column_delete, name='spreadsheets_column_delete'),
    url(r'^spreadsheets/(?P<id>\d+)/edit/row/(?P<rid>\d+)/delete$', views.spreadsheets_row_delete, name='spreadsheets_row_delete'),


    path(r'plots/', views.plots, name='plots'),
    url(r'^plots/add/$', views.plots_add, name="plots_add"),
    url(r'^plots/(?P<id>\d+)/delete/$', views.plots_delete, name='plots_delete'),
    url(r'^plots/(?P<id>\d+)/edit/$', views.plots_edit, name='plots_edit'),

    path(r'reports/', views.reports, name='reports'),
    path(r'reports/add/', views.reports_add, name='reports_add'),
    url(r'^reports/(?P<id>\d+)/delete/$', views.reports_delete, name='reports_delete'),
    url(r'^reports/(?P<id>\d+)/edit/$', views.reports_edit, name='reports_edit'),
    url(r'^reports/(?P<id>\d+)/edit/add_element/$', views.reports_add_element, name='reports_add_element'),
    url(r'^reports/(?P<id>\d+)/edit/element/(?P<eid>\d+)/delete$', views.reports_delete_element, name='reports_delete_element'),
    url(r'^reports/(?P<id>\d+)/preview/$', views.reports_preview, name='reports_preview'),
    url(r'^reports/(?P<id>\d+)/pdf/$', views.reports_pdf, name='reports_pdf'),
]
