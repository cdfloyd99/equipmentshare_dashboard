from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('pl-statement/', views.pl_statement_view, name='pl_statement'),
    path('pl-statement/export/<str:branch_name>/', views.export_pl_to_excel, name='export_pl_to_excel'),
    path('dashboard/export-pdf/<str:branch_name>/', views.export_dashboard_pdf, name='export_dashboard_pdf'),# New route for exporting to Excel
]
