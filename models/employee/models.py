import uuid

from django.core.validators import RegexValidator
from django.db import models
from .validators import birthdate_validator


TRADEPOINTS_JSON_FIELD_SCHEMA = {
    'schema': 'http://json-schema.org/draft-07/schema#',
    'type': 'object',
    'properties': {
        'id': {
            "type": "number",
            "minimum": 1
        },
    },
    'required': ['id', ]
}


class Employee(models.Model):
    """Сотрудники"""
    ROLE = [
        ('Мастер', 'Мастер'),
        ('Управляющий', 'Управляющий'),
        ('Менеджер', 'Менеджер'),
    ]
    uuid = models.CharField(
        max_length=100000,
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=50, null=False, blank=False,
        verbose_name='Имя'
    )
    surname = models.CharField(
        max_length=50, null=False, blank=False,
        verbose_name='Фамилия'
    )
    role = models.CharField(max_length=150, choices=ROLE,
                            null=False, blank=False)
    IIN = models.CharField(
        null=False, blank=False, max_length=12, unique=True,
        verbose_name='ИИН', validators=[RegexValidator(r'^\d{12,12}$')]
    )
    pdf = models.FileField(upload_to='pdf')
    address = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name='Адрес'
    )
    phone = models.CharField(
        max_length=100, null=False, blank=False,
        verbose_name='Телефон'
    )
    birthdate = models.DateField(validators=[birthdate_validator])
    tradepoint = models.ForeignKey(
        'trade_point.TradePoint', on_delete=models.PROTECT,
        related_name='tradepoint_employee', verbose_name='Филиал'
    )

    class Meta:
        verbose_name = "Сотрудники"
        verbose_name_plural = "Сотрудники"
