import json
from django.shortcuts import render, get_object_or_404
from .models import Revenue, Expense, Asset, CompanyInfo, Branch
from django.db.models import Sum
import openpyxl
from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML
from datetime import datetime
from django.utils import timezone
from calendar import month_name

# Helper function to get filtered data based on the selected month/year
def get_filtered_data(branch, selected_month, selected_year):
    revenues = Revenue.objects.filter(branch=branch, date__month=selected_month, date__year=selected_year)
    expenses = Expense.objects.filter(branch=branch, date__month=selected_month, date__year=selected_year)
    return revenues, expenses

# Dashboard View
def dashboard_view(request):
    # Get selected branch, month, and year (default to current)
    selected_branch = request.GET.get('branch', 'alabaster')
    selected_month = int(request.GET.get('month', timezone.now().month))
    selected_year = int(request.GET.get('year', timezone.now().year))

    branch = get_object_or_404(Branch, name__iexact=selected_branch.capitalize())
    all_branches = Branch.objects.all()

    # Generate month list (1 to 12 with names)
    months = [(i, month_name[i]) for i in range(1, 13)]

    # Generate year list (e.g., last 10 years up to the current year)
    years = list(range(2010, timezone.now().year + 1))

    # Filter revenues and expenses based on the selected month/year
    revenues, expenses = get_filtered_data(branch, selected_month, selected_year)

    total_revenue = revenues.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    net_income = total_revenue - total_expense
    profit_margin = (net_income / total_revenue) * 100 if total_revenue > 0 else 0

    # Asset Summary (assuming no date for assets)
    assets = Asset.objects.all()
    asset_types = [asset.type for asset in assets]
    asset_values = [float(asset.value) for asset in assets]

    # EPS Calculation
    company_info = CompanyInfo.objects.first()
    shares_outstanding = company_info.shares_outstanding if company_info else 0
    earnings_per_share = net_income / shares_outstanding if shares_outstanding > 0 else 0

    # Revenue by category for the pie chart
    revenue_breakdown = revenues.values('category__name').annotate(total_amount=Sum('amount')).order_by('category__name')
    expense_breakdown = expenses.values('category__name').annotate(total_amount=Sum('amount')).order_by('category__name')

    # Prepare data for charts
    revenue_categories = [item['category__name'] for item in revenue_breakdown]
    revenue_totals = [item['total_amount'] for item in revenue_breakdown]

    expense_categories = [item['category__name'] for item in expense_breakdown]
    expense_totals = [item['total_amount'] for item in expense_breakdown]

    # Prepare context data
    context = {
        'selected_branch': selected_branch,
        'branch_name': branch.name,
        'all_branches': all_branches,
        'total_revenue': total_revenue,
        'total_expense': total_expense,
        'net_income': net_income,
        'profit_margin': profit_margin,
        'earnings_per_share': earnings_per_share,
        'asset_types_json': json.dumps(asset_types),
        'asset_values_json': json.dumps(asset_values),
        'revenue_categories': json.dumps(revenue_categories),
        'revenue_totals': json.dumps([float(v) for v in revenue_totals]),
        'expense_categories': json.dumps(expense_categories),
        'expense_totals': json.dumps([float(v) for v in expense_totals]),
        'selected_month': selected_month,
        'selected_year': selected_year,
        'months': months,  # Pass months to template
        'years': years,    # Pass years to template
    }
    return render(request, 'dashboard/dashboard.html', context)

# P&L Statement View
def pl_statement_view(request):
    selected_branch = request.GET.get('branch', 'alabaster')
    selected_month = int(request.GET.get('month', timezone.now().month))
    selected_year = int(request.GET.get('year', timezone.now().year))

    branch = get_object_or_404(Branch, name__iexact=selected_branch.capitalize())
    all_branches = Branch.objects.all()

    # Generate month list and year list like in dashboard_view
    months = [(i, month_name[i]) for i in range(1, 13)]
    years = list(range(2010, timezone.now().year + 1))

    revenues, expenses = get_filtered_data(branch, selected_month, selected_year)

    total_revenue = revenues.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    net_income = total_revenue - total_expense

    # Revenue by category for the pie chart
    revenue_breakdown = revenues.values('category__name').annotate(total_amount=Sum('amount')).order_by('category__name')
    
    # Expenses by category for the pie chart
    expense_breakdown = expenses.values('category__name').annotate(total_amount=Sum('amount')).order_by('category__name')

    # Prepare data for charts
    revenue_categories = [item['category__name'] for item in revenue_breakdown]
    revenue_totals = [float(item['total_amount']) for item in revenue_breakdown]  # Convert to float
    
    expense_categories = [item['category__name'] for item in expense_breakdown]
    expense_totals = [float(item['total_amount']) for item in expense_breakdown]  # Convert to float

    context = {
        'selected_branch': selected_branch,
        'branch_name': branch.name,
        'all_branches': all_branches,
        'revenues': revenues,
        'expenses': expenses,
        'total_revenue': total_revenue,
        'total_expense': total_expense,
        'net_income': net_income,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'months': months,  # Pass months to template
        'years': years,    # Pass years to template,
        'revenue_categories': json.dumps(revenue_categories),
        'revenue_totals': json.dumps(revenue_totals),  # Already converted to float
        'expense_categories': json.dumps(expense_categories),
        'expense_totals': json.dumps(expense_totals),  # Already converted to float
    }
    return render(request, 'dashboard/pl_statement.html', context)

# Export P&L to Excel
def export_pl_to_excel(request, branch_name):
    # Get the selected branch object
    branch = get_object_or_404(Branch, name__iexact=branch_name.capitalize())

    # Get selected month and year from request parameters (default to current month/year)
    selected_month = int(request.GET.get('month', timezone.now().month))
    selected_year = int(request.GET.get('year', timezone.now().year))

    # Load Revenue and Expenses for the selected branch and time range
    revenues = Revenue.objects.filter(branch=branch, date__month=selected_month, date__year=selected_year)
    expenses = Expense.objects.filter(branch=branch, date__month=selected_month, date__year=selected_year)

    # Create an Excel workbook and add a worksheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Ensure the sheet title is within 31 characters and doesn't contain invalid characters
    safe_sheet_title = f"PL_{branch_name}_{selected_month}_{selected_year}"[:31]
    sheet.title = safe_sheet_title

    # Write the header row for revenues
    sheet.append(["Revenues"])
    sheet.append(["Description", "Category", "Amount ($)"])
    for revenue in revenues:
        sheet.append([revenue.description, revenue.category.name if revenue.category else "N/A", float(revenue.amount)])

    # Write the total revenue row
    total_revenue = sum(float(item.amount) for item in revenues)
    sheet.append(["", "Total Revenue", total_revenue])

    # Leave an empty row before expenses
    sheet.append([])

    # Write the header row for expenses
    sheet.append(["Expenses"])
    sheet.append(["Description", "Category", "Amount ($)"])
    for expense in expenses:
        sheet.append([expense.description, expense.category.name if expense.category else "N/A", float(expense.amount)])

    # Write the total expenses row
    total_expense = sum(float(item.amount) for item in expenses)
    sheet.append(["", "Total Expenses", total_expense])

    # Write the net income
    net_income = total_revenue - total_expense
    sheet.append(["", "Net Income", net_income])

    # Prepare the HTTP response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="PL_Statement_{branch_name}_{selected_month}_{selected_year}.xlsx"'

    # Save the workbook to the response
    workbook.save(response)

    return response

# Export Dashboard to PDF
def export_dashboard_pdf(request, branch_name):
    # Get selected month/year from the request
    selected_month = int(request.GET.get('month', timezone.now().month))
    selected_year = int(request.GET.get('year', timezone.now().year))

    # Get the selected branch
    branch = get_object_or_404(Branch, name__iexact=branch_name.capitalize())

    # Fetch revenues and expenses for the branch, filtered by month/year
    revenues = Revenue.objects.filter(branch=branch, date__month=selected_month, date__year=selected_year)
    expenses = Expense.objects.filter(branch=branch, date__month=selected_month, date__year=selected_year)

    # Calculate totals
    total_revenue = sum(float(item.amount) for item in revenues)
    total_expense = sum(float(item.amount) for item in expenses)
    net_income = total_revenue - total_expense

    # Prepare context data for rendering the PDF
    context = {
        'branch_name': branch.name,
        'revenues': revenues,
        'expenses': expenses,
        'total_revenue': total_revenue,
        'total_expense': total_expense,
        'net_income': net_income,
        'selected_month': selected_month,
        'selected_year': selected_year,
    }

    # Load the HTML template for the dashboard/P&L statement
    template = get_template('dashboard/pdf_template.html')
    html = template.render(context)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Dashboard_P&L_{branch_name}_{selected_month}_{selected_year}.pdf"'

    # Convert the HTML to a PDF
    HTML(string=html).write_pdf(response)

    return response
