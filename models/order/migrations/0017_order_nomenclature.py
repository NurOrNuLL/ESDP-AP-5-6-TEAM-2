# Generated by Django 4.0.4 on 2022-06-26 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclature', '0009_alter_nomenclature_name'),
        ('order', '0016_alter_order_jobs'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='nomenclature',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='nomenclature.nomenclature'),
            preserve_default=False,
        ),
    ]
