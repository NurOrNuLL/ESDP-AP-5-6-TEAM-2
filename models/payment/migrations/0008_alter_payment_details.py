# Generated by Django 4.0.5 on 2022-07-06 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_alter_payment_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='details',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
