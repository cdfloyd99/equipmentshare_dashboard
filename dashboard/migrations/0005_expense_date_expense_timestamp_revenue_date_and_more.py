# Generated by Django 5.1.2 on 2024-10-14 04:45

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_branch_category_alter_expense_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='expense',
            name='timestamp',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='revenue',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='revenue',
            name='timestamp',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
