# Generated by Django 4.0.4 on 2022-06-26 19:31

import django.core.validators
from django.db import migrations, models
from models.employee import validators


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0006_alter_employee_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='IIN',
            field=models.CharField(max_length=12, unique=True, validators=[django.core.validators.RegexValidator('^\\d{12,12}$'), validators.validate_iin], verbose_name='ИИН'),
        ),
    ]
