# dashboard/views.py

import json
from django.shortcuts import render
from .models import Revenue, Expense, Asset, CompanyInfo

def dashboard_view(request):
    # Financial Summary
    total_revenue = sum(float(item.amount) for item in Revenue.objects.all())
    total_expense = sum(float(item.amount) for item in Expense.objects.all())
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

    # Serialize data to JSON strings
    asset_types_json = json.dumps(asset_types)
    asset_values_json = json.dumps(asset_values)

    # Serialize financial data for charts
    revenue_expense_data = json.dumps({
        'total_revenue': total_revenue,
        'total_expense': total_expense,
        'net_income': net_income,
    })

    context = {
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
        # Revenue and Expense Data
        'revenue_expense_data': revenue_expense_data,
    }
    return render(request, 'dashboard/dashboard.html', context)

def pl_statement_view(request):
    revenues = Revenue.objects.all()
    expenses = Expense.objects.all()
    total_revenue = sum(float(item.amount) for item in revenues)
    total_expense = sum(float(item.amount) for item in expenses)
    net_income = total_revenue - total_expense

    context = {
        'revenues': revenues,
        'expenses': expenses,
        'total_revenue': total_revenue,
        'total_expense': total_expense,
        'net_income': net_income,
    }
    return render(request, 'dashboard/pl_statement.html', context)

