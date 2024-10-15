from django.core.management.base import BaseCommand
from dashboard.models import Revenue, Expense, Branch
import random

class Command(BaseCommand):
    help = 'Deletes half of the records for the Kansas City branch'

    def handle(self, *args, **kwargs):
        # Fetch the Kansas City branch
        kansas_city_branch = Branch.objects.filter(name="Kansas City").first()

        # Ensure the branch exists
        if not kansas_city_branch:
            self.stdout.write(self.style.ERROR("Kansas City branch not found."))
            return

        self.stdout.write(self.style.SUCCESS(f"Found branch: {kansas_city_branch.name}"))

        # Fetch all revenues and expenses for Kansas City
        kansas_city_revenues = Revenue.objects.filter(branch=kansas_city_branch)
        kansas_city_expenses = Expense.objects.filter(branch=kansas_city_branch)

        # Calculate the number of records to delete (half of each)
        num_revenues_to_delete = len(kansas_city_revenues) // 2
        num_expenses_to_delete = len(kansas_city_expenses) // 2

        # Delete half of the records for both revenue and expenses
        if num_revenues_to_delete > 0:
            revenues_to_delete = random.sample(list(kansas_city_revenues), num_revenues_to_delete)
            Revenue.objects.filter(id__in=[r.id for r in revenues_to_delete]).delete()
            self.stdout.write(self.style.SUCCESS(f"Deleted {num_revenues_to_delete} revenue records for Kansas City."))
        else:
            self.stdout.write(self.style.WARNING("No revenue records to delete."))

        if num_expenses_to_delete > 0:
            expenses_to_delete = random.sample(list(kansas_city_expenses), num_expenses_to_delete)
            Expense.objects.filter(id__in=[e.id for e in expenses_to_delete]).delete()
            self.stdout.write(self.style.SUCCESS(f"Deleted {num_expenses_to_delete} expense records for Kansas City."))
        else:
            self.stdout.write(self.style.WARNING("No expense records to delete."))

        self.stdout.write(self.style.SUCCESS('Successfully deleted half of the records for Kansas City.'))
