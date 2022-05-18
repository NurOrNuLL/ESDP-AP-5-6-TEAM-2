from django.db import models
from .category_choices import CATEGORY_CHOICES, MARK_CHOICES
from django.core.validators import MinValueValidator


class Service(models.Model):
    """Услуги"""
    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        verbose_name='Категория'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Название'
    )
    price = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Цена'
    )
    note = models.CharField(
        max_length=200, null=True,
        blank=True, verbose_name='Примечание'
    )
    mark = models.CharField(
        max_length=100, choices=MARK_CHOICES,
        verbose_name='Марка'
    )
    nomenclature = models.ForeignKey(
        'nomenclature.Nomenclature',
        on_delete=models.PROTECT,
        related_name='nomenclature_services',
        verbose_name='Номенклатура'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['name', ]
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
