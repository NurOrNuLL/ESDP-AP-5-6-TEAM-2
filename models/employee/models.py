import uuid

from concurrency.fields import AutoIncVersionField
from django.core.validators import RegexValidator
from django.db import models
from .validators import birthdate_validator, validate_iin, latin_validate, number_validate, \
    latin_surname_validate, len_phone_validate, number_surname_validate


class Employee(models.Model):
    """Сотрудники"""
    ROLE = [
        ('Мастер', 'Мастер'),
        ('Управляющий', 'Управляющий'),
        ('Менеджер', 'Менеджер'),
    ]
    version = AutoIncVersionField()
    uuid = models.CharField(
        max_length=100000,
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=50, null=False, blank=False,
        verbose_name='Имя', validators=[latin_validate, number_validate]
    )
    surname = models.CharField(
        max_length=50, null=False, blank=False,
        verbose_name='Фамилия', validators=[latin_surname_validate, number_surname_validate]
    )
    role = models.CharField(max_length=150, choices=ROLE,
                            null=False, blank=False)
    IIN = models.CharField(
        null=False, blank=False, max_length=12, unique=True,
        verbose_name='ИИН', validators=[RegexValidator(r'^\d{12,12}$'), validate_iin]
    )
    image = models.URLField(null=True, blank=True)
    address = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name='Адрес'
    )
    phone = models.CharField(
        max_length=100, null=False, blank=False,
        verbose_name='Телефон', validators=[len_phone_validate]
    )
    birthdate = models.DateField(validators=[birthdate_validator])
    tradepoint = models.ForeignKey(
        'trade_point.TradePoint', on_delete=models.PROTECT,
        verbose_name='Филиал'
    )

    class Meta:
        verbose_name = "Сотрудники"
        verbose_name_plural = "Сотрудники"
