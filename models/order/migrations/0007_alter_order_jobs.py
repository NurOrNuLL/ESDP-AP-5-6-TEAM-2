# Generated by Django 4.0.4 on 2022-06-09 07:20

from django.db import migrations, models
from models.order import validators


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_alter_order_jobs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='jobs',
            field=models.JSONField(validators=[validators.JSONSchemaValidator(limit_value={'properties': {'Мастера': {'items': {'type': 'number'}, 'type': 'array'}, 'Услуги': {'items': {'properties': {'Гарантия': {'default': False, 'type': 'boolean'}, 'Название услуги': {'maxLength': 500, 'type': 'string'}, 'Цена услуги': {'minimum': 1, 'type': 'integer'}}, 'required': ['Название услуги', 'Цена услуги', 'Гарантия'], 'type': 'object'}, 'type': 'array'}}, 'required': ['Услуги', 'Мастера'], 'schema': 'http://json-schema.org/draft-07/schema#', 'type': 'object'})], verbose_name='Работы'),
        ),
    ]
