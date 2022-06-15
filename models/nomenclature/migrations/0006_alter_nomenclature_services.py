# Generated by Django 4.0.4 on 2022-05-26 09:33

from django.db import migrations, models
from models.nomenclature import validators


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclature', '0005_alter_nomenclature_services'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nomenclature',
            name='services',
            field=models.JSONField(blank=True, default=list, null=True, validators=[validators.JSONSchemaValidator(limit_value={'items': {'properties': {'Категория': {'maxLength': 150, 'type': 'string'}, 'Марка': {'maxLength': 150, 'type': 'string'}, 'Название': {'maxLength': 150, 'type': 'string'}, 'Примечание': {'maxLength': 300, 'type': 'string'}, 'Цена': {'minimum': 1, 'type': 'integer'}}, 'required': ['Категория', 'Название', 'Марка', 'Цена'], 'type': 'object'}, 'schema': 'http://json-schema.org/draft-07/schema#', 'type': 'array'})]),
        ),
    ]