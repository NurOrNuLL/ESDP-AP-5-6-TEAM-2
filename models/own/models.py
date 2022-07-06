from concurrency.fields import AutoIncVersionField
from django.db import models
from models.own.validators import OwnValidator


class Own(models.Model):
    """Собственность"""
    version = AutoIncVersionField()
    name = models.CharField(
        max_length=100, null=False, blank=False,
        verbose_name='Наименование собственности'
    )
    contractor = models.ForeignKey(
        'contractor.Contractor', related_name='owns', verbose_name='Контрагент',
        on_delete=models.PROTECT, null=False, blank=False
    )
    number = models.CharField(
        max_length=50, null=True, blank=True, unique=True, validators=[OwnValidator.int_latin_letter_validator],
        verbose_name='Номер'
    )
    comment = models.CharField(
        max_length=300, null=True, blank=True,
        verbose_name='Комментарий'
    )
    is_part = models.BooleanField(default=False, verbose_name="Зап.часть")

    is_deleted = models.BooleanField(default=False, verbose_name='Удалена')

    def __str__(self: object) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name = 'Собственность'
        verbose_name_plural = 'Собственности'
