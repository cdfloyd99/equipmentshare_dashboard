from django.db import models

class RevenueCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Branch(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Revenue(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('RevenueCategory', on_delete=models.SET_NULL, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)  # Allow null temporarily

    def __str__(self):
        return self.description

class Expense(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('ExpenseCategory', on_delete=models.SET_NULL, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)  # Allow null temporarily

    def __str__(self):
        return self.description

class Asset(models.Model):
    type = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    value = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.type

class CompanyInfo(models.Model):
    shares_outstanding = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Company Info ({self.id})"

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
