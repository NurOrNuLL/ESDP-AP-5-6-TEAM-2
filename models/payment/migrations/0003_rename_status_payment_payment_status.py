# Generated by Django 4.0.4 on 2022-06-04 05:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_alter_payment_method'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='status',
            new_name='payment_status',
        ),
    ]
