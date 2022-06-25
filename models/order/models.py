from django.db import models
from django.core.validators import MinValueValidator
from .validators import JSONSchemaValidator
from concurrency.fields import AutoIncVersionField

ORDER_STATUS_CHOICES = [('В работе', 'В работе'), ('Завершен', 'Завершен')]

JOBS_JSON_SCHEMA = {
    'schema': 'http://json-schema.org/draft-07/schema#',
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'Название услуги': {
                'type': 'string',
                'maxLength': 500
            },
            'Категория услуги': {
                'type': 'string',
                'maxLength': 500
            },
            'Марка услуги': {
                'type': 'string',
                'maxLength': 500
            },
            'Цена услуги': {
                'type': 'integer',
                'minimum': 1
            },
            'Гарантия': {
                'type': 'boolean',
                'default': False
            },
            'Мастера': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'Наименование': {
                            'type': 'string',
                            'maxLength': 500
                        },
                        'ИИН': {
                            'type': 'string',
                            'maxLength': 12
                        }
                    },
                    'required': ['Наименование', 'ИИН'],
                    'additionalProperties': False
                }
            }
        },
        'required': ['Название услуги', 'Категория услуги', 'Марка услуги', 'Цена услуги', 'Гарантия', 'Мастера'],
        'additionalProperties': {'type': 'integer', 'minimum': 0, 'maximum': 10000},
        'maxProperties': 7
    }
}


class Order(models.Model):
    """Заказ-наряд"""
    version = AutoIncVersionField()
    trade_point = models.ForeignKey(
        'trade_point.TradePoint', on_delete=models.PROTECT, null=False, blank=False,
        related_name='branch_orders', verbose_name='Филиал')
    contractor = models.ForeignKey(
        'contractor.Contractor', on_delete=models.PROTECT, null=False, blank=False,
        related_name='orders', verbose_name='Контрагент')
    own = models.ForeignKey(
        'own.Own', on_delete=models.PROTECT, null=False, blank=False,
        related_name='own_orders', verbose_name='Собственность')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    finished_at = models.DateTimeField(null=True, blank=True,
                                       verbose_name="Дата завершения")
    status = models.CharField(max_length=100, null=False, blank=False,
                              choices=ORDER_STATUS_CHOICES, verbose_name='Статус')
    price_for_pay = models.IntegerField(
        null=False, blank=False,
        validators=[MinValueValidator(0)], verbose_name='Сумма с гарантиями')
    full_price = models.IntegerField(
        null=False, blank=False,
        validators=[MinValueValidator(0)], verbose_name='Полная сумма')
    payment = models.ForeignKey(
        'payment.Payment', on_delete=models.PROTECT, null=False,
        blank=False, related_name='payment_orders', verbose_name='Оплата')
    note = models.CharField(max_length=100, null=True,
                            blank=True, verbose_name='Примечание')
    mileage = models.IntegerField(null=True, blank=True,
                                  validators=[MinValueValidator(0)], verbose_name='Пробег')
    jobs = models.JSONField(
        verbose_name='Работы',
        validators=[JSONSchemaValidator(limit_value=JOBS_JSON_SCHEMA)])

    def __str__(self):
        return f'{self.created_at, self.contractor, self.status}'

    class Meta:
        verbose_name = "Заказ-наряд"
        verbose_name_plural = "Заказ-наряды"
