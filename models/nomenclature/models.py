from django.db import models


class Nomenclature(models.Model):
    """Номенклатура"""
    name = models.CharField(
        max_length=100, null=False, blank=False,
        verbose_name='Наименование номенклатуры'
    )
    organization = models.ForeignKey(
        'organization.Organization', verbose_name="Организация",
        on_delete=models.PROTECT, null=False, blank=False
    )
    service = models.ManyToManyField(
        'service.Service', verbose_name='Услуги',
        related_name='organization_service'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Номенклатура"
        verbose_name_plural = "Номенклатуры"
