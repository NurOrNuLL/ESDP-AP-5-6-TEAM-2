# Generated by Django 4.0.4 on 2022-05-18 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contractor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Own',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование собственности')),
                ('number', models.CharField(blank=True, max_length=100, null=True, verbose_name='Номер')),
                ('contractor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contractor.contractor', verbose_name='Контрагент')),
            ],
            options={
                'verbose_name': 'Собственность',
                'verbose_name_plural': 'Собственности',
            },
        ),
    ]