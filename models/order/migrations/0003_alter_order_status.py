# Generated by Django 4.0.4 on 2022-06-04 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_order_trade_point'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('В работе', 'В работе'), ('Завершен', 'Завершен')], max_length=100, verbose_name='Статус'),
        ),
    ]