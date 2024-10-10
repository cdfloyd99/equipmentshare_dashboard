# dashboard/admin.py

from django.contrib import admin
from .models import (
    Revenue,
    Expense,
    RevenueCategory,
    ExpenseCategory,
    Asset,
    CompanyInfo
)

admin.site.register(Revenue)
admin.site.register(Expense)
admin.site.register(RevenueCategory)
admin.site.register(ExpenseCategory)
admin.site.register(Asset)
admin.site.register(CompanyInfo)
