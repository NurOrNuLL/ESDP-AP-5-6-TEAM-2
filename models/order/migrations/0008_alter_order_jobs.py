# Generated by Django 4.0.4 on 2022-06-09 13:33

from django.db import migrations, models
from models.order import validators


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_alter_order_jobs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='jobs',
            field=models.JSONField(validators=[validators.JSONSchemaValidator(limit_value={'items': {'properties': {'Гарантия': {'default': False, 'type': 'boolean'}, 'Мастера': {'items': {'type': 'number'}, 'type': 'array'}, 'Название услуги': {'maxLength': 500, 'type': 'string'}, 'Цена услуги': {'minimum': 1, 'type': 'integer'}}, 'required': ['Название услуги', 'Цена услуги', 'Гарантия', 'Мастера'], 'type': 'object'}, 'schema': 'http://json-schema.org/draft-07/schema#', 'type': 'array'})], verbose_name='Работы'),
        ),
    ]
