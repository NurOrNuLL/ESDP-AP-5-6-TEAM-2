# Generated by Django 4.0.5 on 2022-07-04 14:29

import concurrency.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('own', '0005_alter_own_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='own',
            name='version',
            field=concurrency.fields.AutoIncVersionField(default=0, help_text='record revision number'),
        ),
    ]
