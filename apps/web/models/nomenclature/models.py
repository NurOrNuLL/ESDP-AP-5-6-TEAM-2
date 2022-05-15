from django.db import models
from ..organization import Organization


class Nomenclature(models.Model):
    """Номенклатура"""
    name = models.CharField(
        max_length=100, null=False, blank=False,
        verbose_name='Наименование номенклатуры'
    )
    organization = models.ForeignKey(
        Organization, verbose_name="Организация",
        on_delete=models.PROTECT, null=False, blank=False
    )
    service = models.ManyToManyField(
        'web.Service', verbose_name='Услуги',
        related_name='organization_service'
    )

    def __str__(self):
        return f'{self.name}'
