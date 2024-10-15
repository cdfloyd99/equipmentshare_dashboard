from django.contrib import admin
from .models import (
    Revenue,
    Expense,
    RevenueCategory,
    ExpenseCategory,
    Asset,
    CompanyInfo,
    Branch
)

# Inline for Revenues under Branch
class RevenueInline(admin.TabularInline):
    model = Revenue
    extra = 1  # Allows adding extra revenue entries from the Branch admin page

# Inline for Expenses under Branch
class ExpenseInline(admin.TabularInline):
    model = Expense
    extra = 1  # Allows adding extra expense entries from the Branch admin page

# Branch Admin configuration with inlines for Revenue and Expense
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [RevenueInline, ExpenseInline]  # Displays Revenue and Expense inlines in Branch admin

# Custom Admin for Revenue
@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    list_display = ['description', 'amount', 'category', 'branch', 'date']  # Show the date field in the list view

# Custom Admin for Expense
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['description', 'amount', 'category', 'branch', 'date']

# Admin for RevenueCategory and ExpenseCategory
@admin.register(RevenueCategory)
class RevenueCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Register Asset and CompanyInfo without customizations
admin.site.register(Asset)
admin.site.register(CompanyInfo)
