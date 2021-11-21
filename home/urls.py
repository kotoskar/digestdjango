from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'homepage'),
    path('events', views.events, name = 'events'),
    path('cinema', views.cinema, name = 'cinema'),
]
