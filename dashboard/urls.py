# dashboard/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('pl-statement/', views.pl_statement_view, name='pl_statement'),
    # Removed the reporting URL pattern
    # path('reporting/', views.reporting_view, name='reporting'),
]
