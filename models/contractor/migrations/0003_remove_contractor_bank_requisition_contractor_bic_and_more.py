# Generated by Django 4.0.4 on 2022-05-26 13:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contractor', '0002_rename_organisation_contractor_organization'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contractor',
            name='bank_requisition',
        ),
        migrations.AddField(
            model_name='contractor',
            name='BIC',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='БИК'),
        ),
        migrations.AddField(
            model_name='contractor',
            name='IIC',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='ИИК'),
        ),
        migrations.AddField(
            model_name='contractor',
            name='bank_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Наименование банка'),
        ),
        migrations.AlterField(
            model_name='contractor',
            name='IIN_or_BIN',
            field=models.CharField(max_length=12, unique=True, validators=[django.core.validators.RegexValidator('^\\d{12,12}$')], verbose_name='ИИН/БИН'),
        ),
        migrations.AlterField(
            model_name='contractor',
            name='name',
            field=models.CharField(max_length=150, unique=True, verbose_name='Наименование'),
        ),
    ]