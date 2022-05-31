# Generated by Django 4.0.4 on 2022-05-31 13:33

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from models.employee import validators
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('trade_point', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('uuid', models.CharField(default=uuid.uuid4, editable=False, max_length=100000, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('surname', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('role', models.CharField(choices=[('Мастер', 'Мастер'), ('Управляющий', 'Управляющий'), ('Менеджер', 'Менеджер')], max_length=150)),
                ('IIN', models.CharField(max_length=12, unique=True, validators=[django.core.validators.RegexValidator('^\\d{12,12}$')], verbose_name='ИИН')),
                ('pdf', models.FileField(upload_to='pdf')),
                ('address', models.CharField(max_length=50, verbose_name='Адрес')),
                ('phone', models.CharField(max_length=100, verbose_name='Телефон')),
                ('birthdate', models.DateField(validators=[validators.birthdate_validator])),
                ('tradepoint', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tradepoint_employee', to='trade_point.tradepoint', verbose_name='Филиал')),
            ],
            options={
                'verbose_name': 'Сотрудники',
                'verbose_name_plural': 'Сотрудники',
            },
        ),
    ]
