import json
from django.shortcuts import render, get_object_or_404
from .models import Revenue, Expense, Asset, CompanyInfo, Branch
from django.db.models import Sum

def dashboard_view(request):
    # Get the selected branch from the request parameters (default to Alabaster)
    selected_branch = request.GET.get('branch', 'alabaster')

    # Fetch the Branch object (make sure it exists in your database)
    branch = get_object_or_404(Branch, name__iexact=selected_branch.capitalize())

    # Get all branches for the dropdown menu
    all_branches = Branch.objects.all()

    # Financial Summary from Models
    total_revenue = sum(float(item.amount) for item in Revenue.objects.filter(branch=branch))
    total_expense = sum(float(item.amount) for item in Expense.objects.filter(branch=branch))
    net_income = total_revenue - total_expense
    profit_margin = (net_income / total_revenue) * 100 if total_revenue > 0 else 0

    # Asset Summary
    assets = Asset.objects.all()
    total_asset_value = sum(float(asset.value) for asset in assets)
    asset_types = [asset.type for asset in assets]
    asset_values = [float(asset.value) for asset in assets]

    # EPS Calculation
    company_info = CompanyInfo.objects.first()
    shares_outstanding = company_info.shares_outstanding if company_info else 0
    earnings_per_share = net_income / shares_outstanding if shares_outstanding > 0 else 0

    # Revenue by category for the pie chart
    revenue_breakdown = Revenue.objects.filter(branch=branch).values('category__name').annotate(total_amount=Sum('amount')).order_by('category__name')

    # Expenses by category for the pie chart
    expense_breakdown = Expense.objects.filter(branch=branch).values('category__name').annotate(total_amount=Sum('amount')).order_by('category__name')

    # Prepare data for template
    revenue_categories = [item['category__name'] for item in revenue_breakdown]
    revenue_totals = [item['total_amount'] for item in revenue_breakdown]

    expense_categories = [item['category__name'] for item in expense_breakdown]
    expense_totals = [item['total_amount'] for item in expense_breakdown]

    # Serialize data to JSON for Chart.js
    asset_types_json = json.dumps(asset_types)
    asset_values_json = json.dumps(asset_values)

    # Financial data for charts
    revenue_expense_data = json.dumps({
        'total_revenue': total_revenue,
        'total_expense': total_expense,
        'net_income': net_income,
    })

    context = {
        # Branch-specific data
        'selected_branch': selected_branch,
        'branch_name': branch.name,
        'all_branches': all_branches,  # Pass all branches to the template
        # Financial Summary
        'total_revenue': total_revenue,
        'total_expense': total_expense,
        'net_income': net_income,
        'profit_margin': profit_margin,
        # Asset Summary
        'total_asset_value': total_asset_value,
        'asset_types_json': asset_types_json,
        'asset_values_json': asset_values_json,
        # EPS
        'earnings_per_share': earnings_per_share,
        # Revenue and Expense Breakdown Data
        'revenue_categories': json.dumps(revenue_categories),
        'revenue_totals': json.dumps([float(v) for v in revenue_totals]),
        'expense_categories': json.dumps(expense_categories),
        'expense_totals': json.dumps([float(v) for v in expense_totals]),
        # Revenue and Expense Data
        'revenue_expense_data': revenue_expense_data,
    }
    return render(request, 'dashboard/dashboard.html', context)

def pl_statement_view(request):
    # Get the selected branch from the request parameters (default to Alabaster)
    selected_branch_name = request.GET.get('branch', 'alabaster')

    # Fetch the Branch object based on the selected name (case-sensitive)
    branch = get_object_or_404(Branch, name__iexact=selected_branch_name.capitalize())

    # Get all branches for the dropdown menu
    all_branches = Branch.objects.all()

    # Load Revenue and Expenses for P&L statement based on the branch
    revenues = Revenue.objects.filter(branch=branch)
    expenses = Expense.objects.filter(branch=branch)
    total_revenue = sum(float(item.amount) for item in revenues)
    total_expense = sum(float(item.amount) for item in expenses)
    net_income = total_revenue - total_expense

    # Revenue by category for the pie chart
    revenue_breakdown = Revenue.objects.filter(branch=branch).values('category__name').annotate(total_amount=Sum('amount')).order_by('category__name')

    # Expenses by category for the pie chart
    expense_breakdown = Expense.objects.filter(branch=branch).values('category__name').annotate(total_amount=Sum('amount')).order_by('category__name')

    # Prepare data for template
    revenue_categories = [item['category__name'] for item in revenue_breakdown]
    revenue_totals = [item['total_amount'] for item in revenue_breakdown]

    expense_categories = [item['category__name'] for item in expense_breakdown]
    expense_totals = [item['total_amount'] for item in expense_breakdown]

    context = {
        'selected_branch': selected_branch_name,
        'branch_name': branch.name,
        'all_branches': all_branches,  # Pass all branches to the template
        'revenues': revenues,
        'expenses': expenses,
        'total_revenue': total_revenue,
        'total_expense': total_expense,
        'net_income': net_income,
        # Pass categories and totals for charts
        'revenue_categories': json.dumps(revenue_categories),
        'revenue_totals': json.dumps([float(v) for v in revenue_totals]),
        'expense_categories': json.dumps(expense_categories),
        'expense_totals': json.dumps([float(v) for v in expense_totals]),
    }
    return render(request, 'dashboard/pl_statement.html', context)
