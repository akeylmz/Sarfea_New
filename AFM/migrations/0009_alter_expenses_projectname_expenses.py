# Generated by Django 4.2.7 on 2023-11-25 13:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("AFM", "0008_expenses_projectname_expenses_copy"),
    ]

    operations = [
        migrations.AlterField(
            model_name="expenses",
            name="ProjectName_Expenses",
            field=models.CharField(blank=True, max_length=63, null=True),
        ),
    ]
