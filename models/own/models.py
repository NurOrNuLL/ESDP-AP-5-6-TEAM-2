from django.db import models


class Own(models.Model):
    """Собственность"""
    name = models.CharField(
        max_length=100, null=False, blank=False,
        verbose_name='Наименование собственности'
    )
    contractor = models.ForeignKey(
        'contractor.Contractor', related_name='owns', verbose_name='Контрагент',
        on_delete=models.PROTECT, null=False, blank=False
    )
    number = models.CharField(
        max_length=100, null=True, blank=True,
        verbose_name='Номер'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Собственность'
        verbose_name_plural = 'Собственности'
