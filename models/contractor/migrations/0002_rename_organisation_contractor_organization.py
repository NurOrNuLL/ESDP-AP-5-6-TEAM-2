# Generated by Django 4.0.4 on 2022-05-24 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contractor', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contractor',
            old_name='organisation',
            new_name='organization',
        ),
    ]