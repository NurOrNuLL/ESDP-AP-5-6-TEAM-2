# Generated by Django 4.0.4 on 2022-06-06 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trade_point', '0001_initial'),
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='pdf',
        ),
        migrations.AddField(
            model_name='employee',
            name='image',
            field=models.ImageField(default=1, upload_to='image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employee',
            name='tradepoint',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='trade_point.tradepoint', verbose_name='Филиал'),
        ),
    ]