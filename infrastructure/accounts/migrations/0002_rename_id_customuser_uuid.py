# Generated by Django 4.0.4 on 2022-05-28 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='id',
            new_name='uuid',
        ),
    ]
