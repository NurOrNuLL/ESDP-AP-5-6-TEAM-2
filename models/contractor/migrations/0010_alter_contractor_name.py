# Generated by Django 4.0.4 on 2022-06-28 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contractor', '0009_alter_contractor_bic_alter_contractor_iic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractor',
            name='name',
            field=models.CharField(max_length=150, unique=True, verbose_name='Наименование'),
        ),
    ]