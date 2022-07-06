from django.db import models
from .validators import JSONSchemaValidator

PAYMENT_STATUS_CHOICES = [('Не оплачено', 'Не оплачено'), ('Оплачено', 'Оплачено')]

PAYMENT_JSON_FIELD_SCHEMA = {
    'schema': 'http://json-schema.org/draft-07/schema#',
    'type': 'object',
    'properties': {
        'cash': {
            'type': 'string',
            'maxLength': 100
        },
        'cashless': {
            'type': 'object',
            'properties': {
                'consignment': {
                    'type': 'string',
                    'maxLength': 100
                },
                'invoice': {
                    'type': 'string',
                    'maxLength': 100
                }
            }
        },
        'kaspi': {
            'type': 'string'
        }
    },
    'required': [],
    'additionalProperties': False,
    'maxProperties': 1
}

PAYMENT_JSON_FIELD_SCHEMA_CASH = {
    'schema': 'http://json-schema.org/draft-07/schema#',
    'type': 'object',
    'properties': {
        'cash': {
            'type': 'string',
            'maxLength': 100
        },
    },
    'required': [],
    'additionalProperties': False,
    'maxProperties': 1
}

PAYMENT_JSON_FIELD_SCHEMA_CASHLESS = {
    'schema': 'http://json-schema.org/draft-07/schema#',
    'type': 'object',
    'properties': {
        'cashless': {
            'type': 'object',
            'properties': {
                'consignment': {
                    'type': 'string',
                    'maxLength': 100,
                    'minLength': 1,
                },
                'invoice': {
                    'type': 'string',
                    'maxLength': 100,
                    'minLength': 1,
                }
            },
            'required': ['consignment', 'invoice'],
        }
    },
    'required': ['cashless'],
    'additionalProperties': False,
    'maxProperties': 1
}

PAYMENT_JSON_FIELD_SCHEMA_KASPI = {
    'schema': 'http://json-schema.org/draft-07/schema#',
    'type': 'object',
    'properties': {
        'kaspi': {
            'type': 'string',
            'minLength': 1,
        }
    },
    'required': ['kaspi'],
    'additionalProperties': False,
    'maxProperties': 1
}


class Payment(models.Model):
    """Оплата"""
    payment_status = models.CharField(max_length=100, null=False, blank=False,
                                      choices=PAYMENT_STATUS_CHOICES,
                                      verbose_name='Статус оплаты'
                                      )
    method = models.ForeignKey(
        'payment_method.PaymentMethod', on_delete=models.PROTECT, null=True, blank=True,
        related_name='payments', verbose_name='Способ оплаты'
    )
    details = models.JSONField(null=True, blank=True, default=dict)

    def __str__(self):
        return f'{self.id, self.payment_status, self.method, self.details}'

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"
