# Generated by Django 4.0.4 on 2022-06-18 10:37

import concurrency.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_alter_order_jobs'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='version',
            field=concurrency.fields.AutoIncVersionField(default=0, help_text='record revision number'),
        ),
    ]
