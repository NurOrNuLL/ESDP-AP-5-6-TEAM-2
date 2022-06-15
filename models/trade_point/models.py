from django.db import models


class TradePoint(models.Model):
    """Филиал"""
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
    nomenclature = models.ForeignKey(
        'nomenclature.Nomenclature', verbose_name='Номенклатура',
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = "Филиал"
        verbose_name_plural = "Филиалы"