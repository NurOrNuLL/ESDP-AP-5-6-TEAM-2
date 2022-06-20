from django.db import models
from .validators import JSONSchemaValidator

SERVICE_JSON_FIELD_SCHEMA = {
    'schema': 'http://json-schema.org/draft-07/schema#',
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'Название': {
                'type': 'string',
                'maxLength': 150
            },
            'Категория': {
                'type': 'string',
                'maxLength': 150
            },
            'Примечание': {
                'type': 'string',
                'maxLength': 300
            },
            'Марка': {
                'type': 'string',
                'maxLength': 150
            },
            'Цена': {
                'type': 'integer',
                "minimum": 1
            }
        },
        'required': ['Категория', 'Название', 'Марка', 'Цена'],
        'additionalProperties': False
    }
}


class Nomenclature(models.Model):
    """Номенклатура"""
    name = models.CharField(
        max_length=100, null=False, blank=False, unique=True,
        verbose_name='Наименование номенклатуры'
    )
    organization = models.ForeignKey(
        'organization.Organization', verbose_name="Организация",
        on_delete=models.PROTECT, null=False, blank=False
    )
    services = models.JSONField(
        null=True, blank=True, default=list,
        validators=[JSONSchemaValidator(limit_value=SERVICE_JSON_FIELD_SCHEMA)]
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Номенклатура"
        verbose_name_plural = "Номенклатуры"
        ordering = ('id',)
