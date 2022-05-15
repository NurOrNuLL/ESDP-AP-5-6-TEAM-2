from django.db import models


class TradePoint(models.Model):
    name = models.CharField(
        max_length=250, verbose_name='Название'
    )
    address = models.CharField(
        max_length=150, verbose_name='Адрес',
        null=True, blank=True
    )
    organization = models.ForeignKey(
        'web.Organization', verbose_name="Организация",
        on_delete=models.PROTECT
    )
    nomenclature = models.ForeignKey(
        'web.Nomenclature', verbose_name='Номенклатура',
        on_delete=models.PROTECT
    )
