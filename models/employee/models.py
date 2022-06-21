import uuid
from django.core.validators import RegexValidator
from django.db import models
from .validators import birthdate_validator


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
    image = models.ImageField()
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
        verbose_name='Филиал'
    )

    class Meta:
        verbose_name = "Сотрудники"
        verbose_name_plural = "Сотрудники"
