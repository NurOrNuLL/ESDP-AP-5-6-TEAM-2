from django.db import models
from concurrency.fields import AutoIncVersionField


class TradePoint(models.Model):
    """Филиал"""
    version = AutoIncVersionField()
    name = models.CharField(
        max_length=250, verbose_name='Название'
    )
    address = models.CharField(
        max_length=150, verbose_name='Адрес',
        null=True, blank=True
    )
    organization = models.ForeignKey(
        'organization.Organization', verbose_name="Организация",
        on_delete=models.PROTECT
    )
    nomenclature = models.ManyToManyField(
        'nomenclature.Nomenclature', verbose_name='Номенклатура',
        related_name='trade_points'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Филиал"
        verbose_name_plural = "Филиалы"
