from django.db import models
from django.core.validators import RegexValidator


class Organization(models.Model):
    """Организация"""
    name = models.CharField(
        max_length=250, null=False, blank=False,
        verbose_name='Наименование организации'
    )
    address = models.CharField(
        max_length=150, null=True, blank=True,
        verbose_name='Адрес организации'
    )
    RNN = models.CharField(
        null=False, blank=False, max_length=12,
        validators=[RegexValidator(r'^\d{12,12}$')]
    )
    BIN = models.CharField(
        null=False, blank=False, max_length=12,
        validators=[RegexValidator(r'^\d{12,12}$')]
    )
    bank_requisition = models.CharField(
        max_length=100, null=False, blank=False,
        verbose_name='Реквизиты банка'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"
