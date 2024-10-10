# dashboard/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('pl-statement/', views.pl_statement_view, name='pl_statement'),
]
