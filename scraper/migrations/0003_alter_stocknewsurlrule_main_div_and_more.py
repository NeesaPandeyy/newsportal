# Generated by Django 5.2.1 on 2025-06-22 11:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("scraper", "0002_rename_click_button_stocknewsurlrule_news_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stocknewsurlrule",
            name="main_div",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name="stocknewsurlrule",
            name="rows",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
