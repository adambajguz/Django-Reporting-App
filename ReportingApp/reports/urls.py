from django.urls import path
from reports import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
]