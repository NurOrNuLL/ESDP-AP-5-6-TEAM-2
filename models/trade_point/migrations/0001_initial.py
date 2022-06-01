# Generated by Django 4.0.4 on 2022-05-18 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nomenclature', '0001_initial'),
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TradePoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Название')),
                ('address', models.CharField(blank=True, max_length=150, null=True, verbose_name='Адрес')),
                ('nomenclature', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='nomenclature.nomenclature', verbose_name='Номенклатура')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organization.organization', verbose_name='Организация')),
            ],
            options={
                'verbose_name': 'Филиал',
                'verbose_name_plural': 'Филиалы',
            },
        ),
    ]
